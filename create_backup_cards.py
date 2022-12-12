from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import qrcode
import string


wallet_name = input("Enter wallet name (leave blank to use default -> 'Multisig Backup'): ")
if wallet_name == "":
    wallet_name = "Multisig Backup"

descriptor = ""
while descriptor == "":
    descriptor = input("Paste the 2/3 multisig wallet descriptor from Sparrow Wallet: ")


qr_density = input("Entire desired qr code density as an integer ('21'=S-21x21, '25'=M-25x25, '29'=L-29x29). Leave blank to use default (M): ")
if qr_density == "":
    qr_density = 25
else:
    qr_density = int(qr_density)

def create_card_template(c, width = 3.5*inch, height = 2.5*inch):
    
    # calculate border_width
    border_width = .05*height
    top_border_width = .075*height
    text_size = .6*top_border_width


    # set fill color and solid line
    c.setFillColor('black')
    c.setDash(1,0)

    # create card outline
    c.rect(0, 0, width, -height, fill=1)

    # create border
    c.setFillColor('#941bf7')
    c.setStrokeColor('#941bf7')
    c.roundRect(border_width/2,-(top_border_width-border_width/2),width-border_width,-(height-top_border_width), radius=border_width*1.3, fill=1)
    
    c.setFillColor('white')
    c.setStrokeColor('white')
    c.roundRect(border_width,-top_border_width,width-2*border_width,-(height-top_border_width-border_width), radius=border_width, fill=1)
    
    # add everyday bitcoiner logo and banner
    c.setFont('Helvetica-Bold',text_size)
    c.setStrokeColor('black')
    
    logo_width = 6/15*width
    logo_height = top_border_width*.8
    everyday_bitcoiner_logo_size = 1.2*top_border_width
    bitcoin_logo_height = .8*logo_height
    bitcoin_logo_width = 712/980*bitcoin_logo_height
    c.roundRect((width-logo_width)/2,-top_border_width+border_width/4+logo_height/2,logo_width,-logo_height,radius=logo_height/2,fill=1)
    c.setFillColor('black')
    c.drawCentredString(width/2,-top_border_width-.5,'      Everyday    itcoiner')
    
    logo_x_loc = (width-logo_width)/2
    logo_y_loc = -top_border_width+border_width/4-everyday_bitcoiner_logo_size/2
    c.circle(logo_x_loc+everyday_bitcoiner_logo_size/2,logo_y_loc+everyday_bitcoiner_logo_size/2,r=everyday_bitcoiner_logo_size/2, fill=1)
    c.drawImage('imgs/everyday_bitcoiner_logo.png',logo_x_loc,logo_y_loc,everyday_bitcoiner_logo_size,everyday_bitcoiner_logo_size, mask=[0,1,0,1,0,1])

    c.drawImage('imgs/bitcoin_logo.jpg',.5*width+8,-top_border_width-2.,bitcoin_logo_width,bitcoin_logo_height)

    
    return height, width, top_border_width, border_width 


def draw_qr_code_template(c, size, loc_x = 0, loc_y = 0, num_cols_rows = 25):

    

    # determine the width and height of row and column labels
    row_label_width = 1/20*size
    col_label_height = 1/20*size

    # offset to location
    c.translate(loc_x+row_label_width, loc_y)

    # calculate height and width for each row col
    col_row_size = (size-row_label_width)/num_cols_rows

    # calculate size of grid section
    grid_size = size - row_label_width

    # determine row and col height and width based on number of rows/cols
    if num_cols_rows == 21:
        row_label_height = col_row_size*7
        col_label_width = col_row_size*7
        number_of_labels = 3
    else:
        row_label_height = col_row_size*5
        col_label_width = col_row_size*5
        number_of_labels = 5

    # create arrays for making qr code grid
    col_row_array = [x*col_row_size for x in range(0,num_cols_rows+1)]
    
    row_label_height_array = [x*row_label_height for x in range(0,number_of_labels+1)]
    row_label_width_array = [0, - row_label_width]

    col_label_width_array = [x*col_label_width for x in range(0,number_of_labels+1)]
    col_label_height_array = [grid_size,grid_size+col_label_height]
    
    # Add extra label for size 29 qr code
    if num_cols_rows == 29:
        row_label_height_array.append(grid_size)
        col_label_width_array.append(grid_size)

    # Format and create grid
    c.setDash(1,.5)
    c.setLineWidth(.15)
    c.grid(col_row_array, col_row_array)

    # Format and create labels
    c.setDash(1,0)
    c.setLineWidth(1)
    c.grid(row_label_width_array, row_label_height_array)
    c.grid(col_label_width_array, col_label_height_array)
    c.grid(col_label_width_array, row_label_height_array)
    c.setLineWidth(0.25)

    if num_cols_rows == 21:
        row_labels = list(string.ascii_uppercase)[0:3]
        col_labels = [x+1 for x in range(3)]
    elif num_cols_rows == 25:
        row_labels = list(string.ascii_uppercase)[0:5]
        col_labels = [x+1 for x in range(5)]
    else:
        row_labels = list(string.ascii_uppercase)[0:6]
        col_labels = [x+1 for x in range(6)]

    row_label_loc_height_array = []
    col_label_loc_width_array = []
    
    for i in range(len(row_label_height_array)-1):
        row_label_loc_height_array.append((row_label_height_array[i]+row_label_height_array[i+1])/2)
        col_label_loc_width_array.append((col_label_width_array[i]+col_label_width_array[i+1])/2)

    row_label_x_pos = (row_label_width_array[0]+row_label_width_array[1])/2
    col_label_y_pos = (col_label_height_array[0]+col_label_height_array[1])/2

    font_size = size/25
    
    font_offset_down = size/75
    
    
    c.setFont('Helvetica',font_size)

    for i in range(len(row_labels)):
        c.drawCentredString(row_label_x_pos, row_label_loc_height_array[-1-i]-font_offset_down,row_labels[i])
        c.drawCentredString(col_label_loc_width_array[i], col_label_y_pos-font_offset_down, str(col_labels[i]))

    # Add 3 qr orientation markers
    for j in range(3):

        c.setFillColor('black')
        c.rect(0,0,7*col_row_size,7*col_row_size,fill=1)
        c.setFillColor('white')
        c.rect(1*col_row_size,1*col_row_size,5*col_row_size,5*col_row_size,fill=1)
        c.setFillColor('black')
        c.rect(2*col_row_size,2*col_row_size,3*col_row_size,3*col_row_size,fill=1)

        if j == 0:
            # Shift to top left marker
            c.translate(0,(grid_size-7*col_row_size))
        elif j == 1:
            # Shift to top right marker
            c.translate((grid_size-7*col_row_size),0)
        else:
            # Shift back to origin
            c.translate(-(grid_size-7*col_row_size),-(grid_size-7*col_row_size))

    c.translate(-loc_x-row_label_width, -loc_y)
    return

# Split out each key info for descriptor
descriptor = descriptor.split(',')

key_info_1 = descriptor[1]
key_info_2 = descriptor[2]
key_info_3 = descriptor[3].split(')')[0]


# Split out information for each key
fingerprint1= key_info_1.split(']')[0][1:9]
xpub1 = key_info_1.split(']')[1].split('/')[0]
derivation1 = 'm/'+key_info_1.split(']')[0][10:].replace('h','\' ')
key_info_1_qrcode = qrcode.make(key_info_1)
key_info_1_qrcode.save("qrcodes/key_info_1_qrcode.png")

fingerprint2= key_info_2.split(']')[0][1:9]
xpub2 = key_info_2.split(']')[1].split('/')[0]
derivation2 = 'm/'+key_info_2.split(']')[0][10:].replace('h','\' ')
key_info_2_qrcode = qrcode.make(key_info_2)
key_info_2_qrcode.save("qrcodes/key_info_2_qrcode.png")

fingerprint3= key_info_3.split(']')[0][1:9]
xpub3 = key_info_3.split(']')[1].split('/')[0]
derivation3 = 'm/'+key_info_3.split(']')[0][10:].replace('h','\' ')
key_info_3_qrcode = qrcode.make(key_info_3)
key_info_3_qrcode.save("qrcodes/key_info_3_qrcode.png")

# Make a dictionary to loop through later
wallet_description = {"key1":
                            {'key_number':1,
                             'fp': fingerprint1,
                             'xpub': xpub1,
                             'derivation': derivation1,
                             'qr_code': 'qrcodes/key_info_1_qrcode.png'},
                      "key2":
                            {'key_number':2,
                             'fp': fingerprint2,
                             'xpub': xpub2,
                             'derivation': derivation2,
                             'qr_code': 'qrcodes/key_info_2_qrcode.png'},
                      "key3":
                            {'key_number':3,
                             'fp': fingerprint3,
                             'xpub': xpub3,
                             'derivation': derivation3,
                             'qr_code': 'qrcodes/key_info_3_qrcode.png'}}

# Create pdf canvas and set starting point
c = canvas.Canvas(wallet_name.replace(" ","_")+"_multi_sig_backup.pdf", pagesize = letter)
c.translate(0.5*inch, 10.5*inch)

num_keys = 3

for i in range(num_keys):

    # create template and grab dimensions
    height, width, top_border_width, border_width = create_card_template(c)
    top_padding = border_width
    object_padding = .5*border_width
    text_box_height = 1.1*border_width
    font_size = 0.8*text_box_height

    # Draw Qr Code
    qr_size = height - top_border_width - object_padding*2 - top_padding - text_box_height - border_width
    qr_x_loc = width - border_width - object_padding - qr_size
    qr_y_loc = -height + border_width + 2*object_padding + text_box_height

    draw_qr_code_template(c, qr_size, qr_x_loc, qr_y_loc, qr_density)

    
    c.setLineWidth(1)
    c.setFont('Helvetica', font_size)
    
    # Draw key numbering
    key_num_box_width = (qr_size-object_padding)*1/3
    key_size = 0.8*text_box_height
    key_num_x_loc = width - border_width - object_padding - key_num_box_width
    key_num_y_loc = -height + border_width + object_padding

    c.drawImage('imgs/keys.jpg',key_num_x_loc+2.5,key_num_y_loc+ text_box_height/2 - key_size/2,width=key_size,height=key_size)
    c.roundRect(key_num_x_loc, key_num_y_loc, key_num_box_width, text_box_height, radius=text_box_height/2)
    c.drawCentredString(key_num_x_loc+key_size/2 + key_num_box_width/2, key_num_y_loc+ text_box_height/4.5, str(wallet_description['key'+str(i+1)]['key_number'])+"/3")



    # Draw fingerprint
    fp_box_width = (qr_size-object_padding)*2/3
    fp_size = .8*text_box_height
    fp_x_loc = width - border_width - 2*object_padding - key_num_box_width - fp_box_width
    fp_y_loc = -height + border_width + object_padding
    
    c.drawImage('imgs/fingerprint.jpg',fp_x_loc+2.5,fp_y_loc + text_box_height/2 - fp_size/2,width=fp_size,height=fp_size)
    c.roundRect(fp_x_loc,fp_y_loc,fp_box_width,text_box_height, radius=text_box_height/2)
    c.drawCentredString(fp_x_loc+fp_size/2+ (fp_box_width)/2,fp_y_loc + text_box_height/4.5,wallet_description['key'+str(i+1)]['fp'])

    # Draw Title
    title_box_width = width - 2*border_width-3*object_padding-qr_size
    title_x_loc = border_width+object_padding
    title_y_loc = -top_border_width-top_padding
    title_box_height = 1.25*text_box_height
    title_font_size = .8*title_box_height
    c.setFont('Helvetica-Bold', title_font_size)

    c.roundRect(title_x_loc,title_y_loc,title_box_width,-title_box_height, radius=text_box_height/4)
    c.drawCentredString(border_width+object_padding+title_box_width/2, -top_border_width-top_padding-title_box_height+ title_box_height/4.5,wallet_name)

    # Draw Spots for 12 words
    to = c.beginText(border_width+object_padding,-top_border_width-top_padding-title_box_height-object_padding-.6*text_box_height)
    secret_words_font_size = font_size*1.15
    to.setFont('Helvetica',secret_words_font_size)
    to.setFillColor('black')
    for i in range(12):
        if i < 9:
            to.textLine(text=str(i+1)+":________________")
        else:
            to.textLine(text=str(i+1)+":_______________")

    c.drawText(to)


    c.translate(0,-2.75*inch)



# Start new page and set starting point
c.showPage()
c.translate(4.5*inch, 10.5*inch)

for key in wallet_description:

    if wallet_description[key]["key_number"] != 3:
        c.translate(0,-2.75*inch)
    else:
        c.translate(0,+2*2.75*inch)


    height, width, top_border_width, border_width = create_card_template(c)

    

    # Draw Title
    title_box_width = width - 2*border_width-3*object_padding-qr_size
    title_x_loc = border_width+object_padding
    title_y_loc = -top_border_width-top_padding
    title_box_height = 1.25*text_box_height
    title_font_size = .8*title_box_height
    c.setFont('Helvetica', font_size)

    # Add xpub title with key logo
    c.drawImage('imgs/keys.jpg',title_x_loc+2.5,title_y_loc- text_box_height/2 - key_size/2,width=key_size,height=key_size)
    c.roundRect(title_x_loc,title_y_loc,title_box_width,-text_box_height, radius=text_box_height/2)
    c.drawCentredString(border_width+object_padding+title_box_width/2, -top_border_width-top_padding-text_box_height+ text_box_height/4.5,"#"+str(wallet_description[key]['key_number'])+" xpub")

    # Add xpub qr code
    c.drawImage(wallet_description[key]['qr_code'],qr_x_loc-.025*qr_size,qr_y_loc-.025*qr_size,width = qr_size*1.05,height=qr_size*1.05)

    # Add Xpub
    to = c.beginText(border_width+object_padding,-top_border_width-top_padding-title_box_height-object_padding-.6*text_box_height)
    xpub_font_size = font_size*1.4
    to.setFont('Helvetica',xpub_font_size)
    to.setFillColor('black')
    i = 0
    for i in wallet_description[key]['xpub']:
        if to.getCursor()[0] >= (border_width+title_box_width):
            to.moveCursor(0,13)
        to.textOut(i)
        to.setFont('Helvetica',xpub_font_size/2)
        to.textOut(" ")
        to.setFont('Helvetica',xpub_font_size)


   

    c.drawText(to)

    

    # Add derivation path
    c.setFont('Helvetica',font_size)
    c.roundRect(fp_x_loc,fp_y_loc,qr_size,text_box_height, radius=text_box_height/2)
    c.drawCentredString(fp_x_loc+(qr_size)/2,fp_y_loc + text_box_height/4.5,wallet_description[key]['derivation'])

c.save()
