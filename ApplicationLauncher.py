# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 13:46:39 2022

@author: bitam
"""
"""111111111111111111111111"""

import sqlite3
import PySimpleGUI as sg
from datetime import datetime
import random
con = sqlite3.connect('database.db')
cur = con.cursor()
default_window_size = (1000, 600)
running = True
login_SSN = 0
au_ID = 0
bids_list=[]
auction_list = []
payment_info = []

def initial_window():

    global window

    layout = [[sg.Text('', size=(20, 4))],
              [sg.Button('Buyer', size=20)],
              [sg.Button('Seller', size=20)],
              [sg.Button('Admin', size=20)],
              [sg.Exit(size=(20))]]

    return sg.Window('Initial Page', layout, size=default_window_size, element_justification='c')


def seller_initial_window():

    global window

    layout = [[sg.Text('', size=(20, 4))],
              [sg.Button('Login', key="seller_login", size=20)],
              [sg.Button('Sign UP', key="seller_signup", size=20)],
              [sg.Button('Back to Main Menu', size=20)],
              [sg.Exit(size=(20))]]

    return sg.Window('Seller initial window', layout, size=default_window_size, element_justification='c')


def seller_signup_window():
    layout = [[sg.Text('', size=(25, 4))],
              [sg.Text('', size=(5, 1)), sg.Text('SSN', size=(22, 1)),
               sg.Input(key='seller_ssn', size=30)],
              [sg.Text('', size=(5, 1)), sg.Text('Password', size=(
                  22, 1)), sg.Input(key='seller_password', size=30)],
              [sg.Text('', size=(5, 1)), sg.Text('IBAN', size=(22, 1)),
               sg.Input(key='seller_iban', size=30)],
              [sg.Text('', size=(5, 1)), sg.Text('Name', size=(22, 1)),
               sg.Input(key='seller_name', size=30)],
              [sg.Text('', size=(5, 1)), sg.Text('Surname', size=(22, 1)),
               sg.Input(key='seller_surname', size=30)],
              [sg.Text('', size=(5, 1)), sg.Text('Birth', size=(22, 1)), sg.Input(
                  key='seller_birth_date', size=(15, 1)), sg.CalendarButton('Choose Date', format='%Y-%m-%d')],
              [sg.Text('', size=(5, 1)), sg.Text('', size=(22, 1)), sg.Button(
                  'Sign-Up', key="seller_signup_button", size=9, bind_return_key=True)],
              [sg.Text('', size=(5, 1)), sg.Text('', size=(22, 1)), sg.Button(
                  'Go Back', key="return_seller_initial_page", size=9)],
              [sg.Exit(size=(25))]]
    return sg.Window('Sign-Up Page', layout, size=default_window_size, element_justification='c')


def seller_login_window():
    layout = [[sg.Text('', size=(20, 4))],
              [sg.Text('SSN', size=20), sg.Input(key='seller_ssn', size=30)],
              [sg.Text('password', size=20), sg.Input(
                  key='seller_password', size=30)],
              [sg.Button('Log in', key='seller_login_button', size=20)],
              [sg.Button('Go Back', key="return_seller_initial_page", size=20)],
              [sg.Exit(size=(20))]]
    return sg.Window('Seller login window', layout, size=default_window_size, element_justification='c')


def seller_signup_button(values):

    global window
    x = True
    while True:
        today = datetime.now()
        if values['seller_ssn'] == '':
            sg.popup("Seller SSN should not be empty")
            break
        elif not values['seller_ssn'].isnumeric():
            sg.popup("Seller SSN should be numeric!")
            break
        elif not len(str(values['seller_ssn'])) == 11:
            sg.popup("Length of seller SSN should be 11")
            break
        elif values['seller_password'] == '':
            sg.popup("Seller Password should not be empty")
            break
        elif values['seller_iban'] == '':
            sg.popup("Seller IBAN should not be empty")
            break
        elif not values['seller_iban'].isnumeric():
            sg.popup("Seller IBAN should be numeric!")
            break
        elif not len(str(values['seller_iban'])) == 24:
            sg.popup("Length of seller IBAN should be 24")
            break
        elif values['seller_name'] == '':
            sg.popup("Seller Name should not be empty")
            break
        elif values['seller_surname'] == '':
            sg.popup("Seller Surname should not be empty")
            break
        elif values['seller_name'].isnumeric():
            sg.popup("Seller Name should not contain numeric values!")
            break
        elif values['seller_surname'].isnumeric():
            sg.popup("Seller surName should not contain numeric values!")
            break
        elif x:
            try:
                birth_date = datetime.strptime(values["seller_birth_date"], '%Y-%m-%d')
                if (today-birth_date).days < 0:
                    sg.popup("Birthday cannot be in the future")
                    break
                elif (today-birth_date).days < 6570:
                    sg.popup("An Buyer should be above 18 years old!")
                    break
            except:
                sg.popup("Buyer birthdate should not be empty")
                break
            x = False
        elif (today-birth_date).days < 0:
            sg.popup("Birthday cannot be in the future")
            break
        elif (today-birth_date).days < 6570:
            sg.popup("Seller should be above 18 years old!")
            break
        else:
            unique_ssn = True
            cur.execute('SELECT sellerSSN FROM Seller')
            row = cur.fetchall()
            for tuple_ in row:
                
                if int(values['seller_ssn']) == tuple_[0]:
                    unique_ssn = False
                    break
            if not unique_ssn:
                sg.popup('This SSN is already in use.')
                break
            seller_name = values['seller_name']
            seller_surname = values['seller_surname']
            seller_SSN = values['seller_ssn']
            seller_iban = values['seller_iban']
            new_iban = f"TR{seller_iban}"
            seller_password = values['seller_password']
            seller_birthday = values['seller_birth_date']
            cur.execute('''INSERT INTO Seller VALUES (?,?,?,?,?,?)''', (seller_SSN,
                        new_iban, seller_name, seller_surname, seller_password, seller_birthday))
            sg.popup(f'Welcome to our app, {seller_name}!')
            window.close()
            window = seller_login_window()
            con.commit()
            break


def seller_main_window():
    global window

    layout = [[sg.Text('', size=(20, 4))],
              [sg.Button('New Auction', key="new_auction", size=20)],
              [sg.Button('My Auctions', key='my_auctions', size=20)],
              [sg.Button('Refresh',key= "refresh", size=20)],
              [sg.Button('Log Out', key='seller_log_out', size=20)]]

    return sg.Window('Seller main window', layout, size=default_window_size, element_justification='c')


def seller_login_button(values):

    global login_SSN
    global window

    # get the seller ssn from the input
    s_ssn = values['seller_ssn']
    s_password = values['seller_password']

    # if no ssn is entered, give error message.
    if s_ssn == '':
        sg.popup('SSN cannot be empty!')
    elif s_password == '':
        sg.popup('Password cannot be empty!')

    # if a ssn and a password is entered, check if it is in the Seller table of the database.
    # if it is not in the Seller table, give error message.
    # if it is in the Seller table, proceed with the corresponding seller ssn.
    else:
        cur.execute(
            'SELECT sellerSSN FROM Seller WHERE sellerSSN = ? AND Spassword = ?', (s_ssn, s_password))
        row = cur.fetchone()
        if row is None:
            sg.popup('Either ssn or password is wrong!')
        else:
            login_SSN = row[0]
            window.close()
            window = seller_main_window()



def new_auction_window():
    global random_admin_ID
    admin_list = []
    for row in cur.execute('SELECT adminSSN, AFName, ALName FROM Admin'):
        admin_list.append(row[0])
    random_admin_index = random.randint(0,len(admin_list)-1)
    random_admin_ID = admin_list[random_admin_index]
    
    category_list = [(0, "All Categories")]
    for row in cur.execute('SELECT  cID, name FROM Category'):
        category_list.append((row[0], row[1]))

    layout = [[sg.Text('', size=(25, 2))],
              [sg.Text('Categories:', size=(10, 1)),
               sg.Combo(category_list, size=(50, 10), key='category')],
              [sg.Text('', size=(5,1)), sg.Text(f"Controller Admin ID = {random_admin_ID}", size=30)],
              [sg.Text('', size=(5, 1)), sg.Text('Description', size=(
                  22, 1)), sg.Input(key='new_auction_description', size=30)],
              [sg.Text('', size=(5, 1)), sg.Text('Title', size=(22, 1)),
               sg.Input(key='new_auction_title', size=30)],
              [sg.Text('', size=(5, 1)), sg.Text('Buy it Now Price',
                                                 size=(22, 1)), sg.Input(key='bin_price', size=30)],
              [sg.Text('', size=(5, 1)), sg.Text('Starting Price', size=(
                  22, 1)), sg.Input(key='new_starting_price', size=30)],
              [sg.Text('', size=(5, 1)), sg.Text('Start Date', size=(22, 1)), sg.Input(
                  key="start_date", size=(15, 1)), sg.CalendarButton('Choose Date', format='%Y-%m-%d %H:%M:%S')],
              [sg.Text('', size=(5, 1)), sg.Text('End Date', size=(22, 1)), sg.Input(
                  key="end_date", size=(15, 1)), sg.CalendarButton('Choose Date', format='%Y-%m-%d %H:%M:%S')],
              [sg.Text('', size=(10, 1)), sg.Button(
                  'Save', key='save_new_auction', size=20)],
              [sg.Text('', size=(10, 1)), sg.Button('Return to Main Menu', key='return_seller_main_page', size=20)]]

    return sg.Window('Create a New Auction Page', layout, size=default_window_size)


def seller_save_button(values):
    global random_admin_ID
    global window

    while True:

        today_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        end_date = 'Null'
        current_price = 0
        status = "NotAccepted"
        au_ID = []
        cur.execute('SELECT auID FROM Auction')
        row = cur.fetchall()
        for aid in row:
            au_ID.append(aid[0])
        new_au_id = max(au_ID) + 1
        seller_ssn = login_SSN

        if values['category'] == '':
            sg.popup("A category should be chosen")
            break
        elif values['new_auction_title'] == '':
            sg.popup("Title should not be empty")
            break
        elif values['bin_price'] == '':
            sg.popup("Buy it now price should not be empty")
            break
        elif not values['bin_price'].isnumeric():
            sg.popup("Buy it now price should be numeric!")
            break
        elif values['new_starting_price'] == '':
            sg.popup("Starting price should not be empty")
            break
        elif not values['new_starting_price'].isnumeric():
            sg.popup("Starting price should be numeric")
            break
        elif int(values['bin_price']) <= int(values['new_starting_price']):
            sg.popup("Starting price should be less than buy it now price")
            break
        elif values["start_date"] > values["end_date"]:
            sg.popup("Starting date should be scheduled before end date")
            break
        elif today_date > values["start_date"] or today_date > values["end_date"]:
            sg.popup("Starting date and end date should be scheduled after today")
            break
        else:

            auction_id = new_au_id
            admin_ssn = random_admin_ID
            seller_SSN = seller_ssn
            category_id = values['category'][0]
            description = values['new_auction_description']
            title = values['new_auction_title']
            bin_price = values['bin_price']
            current_price = 0
            status = 'NotAccepted'
            start_price = 0
            start_date = datetime.today().strftime('%Y-%m-%d')
            end_date = values["end_date"]
            cur.execute('''INSERT INTO Auction VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''', (auction_id, admin_ssn, seller_SSN, category_id,
                                                                                     description, title, bin_price, current_price,
                                                                                     status, start_price, start_date, end_date, 'NotPaid'))
            sg.popup('The auction is created!')
            window.close()
            window = new_auction_window()
            con.commit()
            break
def list_bids_button(values):
    global window
    if values["active_auctions"][8] == 'Ongoing':
        try:
            values["active_auctions"][8] == 'Ongoing'
            bids_list = []
            auction_id = values['active_auctions'][0]
            for row in cur.execute('SELECT bidID, bidPrice, buyerSSN, auID FROM Bid WHERE auID = ?', (auction_id,)):
                bids_list.append([row[0], row[1], row[2], row[3]])
                
            bids_list.sort(key= lambda bids_list : bids_list[1], reverse=True)
            window.Element('bids').Update(values = bids_list)
        except:
            sg.popup("An ongoing auction should be chosen")
    else:
        sg.popup("An ongoing auction should be chosen")
        
def active_auction_window():
    global window
    active_auctions = []
    seller_SSN = login_SSN
    cur.execute(f'SELECT * FROM Auction where sellerSSN={seller_SSN}')
    all_auctions = cur.fetchall()
    for auction in all_auctions:
        active_auctions.append(auction)
    
    layout = [[sg.Text('', size=(25,2))],
               [sg.Text('Auctions:', size=(10,10)),
               sg.Combo(active_auctions,key="active_auctions",size=(60, 10))],
               [sg.Text('', size=(10,1)), sg.Button('Check Bill',key = "check_bill", size=30)],
               [sg.Text('', size=(10,1)), sg.Button('Delete Auction',key = "delete_auction", size=30)],
               [sg.Text('', size=(10,1)), sg.Button('Return to Main Menu',key = "return_seller_main_page", size=30)],
               [sg.Text('', size=(10,1)), sg.Button('List Bids', key = 'bid_list')],
               [sg.Text('Bids:', size=(10,10)), sg.Listbox(bids_list, size=(50, 10), key='bids', select_mode='multiple')],
               [sg.Exit(size=(20))]] 
    
    return sg.Window('Active auction page', layout, size=default_window_size, element_justification='c')


def check_bill_button(values):
    global window
    global auID
    while True:
        if values["active_auctions"] == '':
            sg.popup("An auction should be chosen for this function")
            break
        elif values["active_auctions"][8] != 'Finished':
            sg.popup(
                "Chosen auction's status should be -finished- for this function")
            break
        else:
            auID = values["active_auctions"][0]
            window.close()
            window = bill_window()
            con.commit()
            break


def bill_window():
    global window
    global auID
    selected_auID = auID
    cur.execute(
        f'SELECT bil.transNum, bil.netAmount, bil.sellerSSN, bil.winnerSSN FROM Billing b, Bill bil WHERE b.auID = {selected_auID} and b.transNum = bil.transNum')
    bill = cur.fetchall()

    layout = [[sg.Text('', size=(25, 2))],
              [sg.Text('', size=(5, 1)), sg.Text(f'{bill}', size=30)],
              [sg.Text('', size=(10, 1)), sg.Button('Return to Main Menu', key='return_seller_main_page', size=20)]]

    return sg.Window('Bill Information', layout, size=default_window_size)

def delete_auction_button(values):
    global window
    global auID
    try:
        auID = values["active_auctions"][0]
        selected_auID = auID
        x=True
    except:
        sg.popup("An auction should be selected for this function")
        x=False
    while x:
        if values["active_auctions"] == '':
            sg.popup("An auction should be selected for this function")
            break
        elif values["active_auctions"][8] != 'Ongoing':
            sg.popup("Only ongoing auctions can be deleted")
            break
        else:
            cur.execute(f'Delete FROM Auction WHERE auID = {selected_auID}')
            con.commit()
            window.close()
            window = seller_main_window()
            break


def buyer_initial_window():

    global window

    layout = [[sg.Text('', size=(20, 4))],
              [sg.Button('Login', key="buyer_login", size=20)],
              [sg.Button('Sign up', key="buyer_signup", size=20)],
              [sg.Button('Back to Main Menu', size=20)],
              [sg.Exit(size=(20))]]

    return sg.Window('buyer initial window', layout, size=default_window_size, element_justification='c')


def buyer_login_window():

    layout = [[sg.Text('', size=(20, 4))],
              [sg.Text('SSN', size=20), sg.Input(key='buyer_ssn', size=30)],
              [sg.Text('password', size=20), sg.Input(
                  key='buyer_password', size=30)],
              [sg.Button('Log in', key='buyer_login_button', size=20)],
              [sg.Button('Go Back',key= "return_buyer_initial_page", size=20)]]
    return sg.Window('buyer login window', layout, size=default_window_size, element_justification='c')


def buyer_signup_window():
    layout = [[sg.Text('', size=(25, 4))],
              [sg.Text('', size=(5, 1)), sg.Text('SSN', size=(22, 1)),
               sg.Input(key='buyer_ssn', size=30)],
              [sg.Text('', size=(5, 1)), sg.Text('Password', size=(
                  22, 1)), sg.Input(key='buyer_password', size=30)],
              [sg.Text('', size=(5, 1)), sg.Text('Name', size=(22, 1)),
               sg.Input(key='buyer_name', size=30)],
              [sg.Text('', size=(5, 1)), sg.Text('Surname', size=(22, 1)),
               sg.Input(key='buyer_surname', size=30)],
              [sg.Text('', size=(5, 1)), sg.Text('Birth', size=(22, 1)), sg.Input(
                  key='buyer_birth_date', size=(15, 1)), sg.CalendarButton('Choose Date', format='%Y-%m-%d')],
              [sg.Text('', size=(5, 1)), sg.Text('', size=(22, 1)), sg.Button(
                  'Sign-Up', key="buyer_signup_button", size=9, bind_return_key=True)],
              [sg.Text('', size=(5, 1)), sg.Text('', size=(22, 1)),
               sg.Button('Go Back', key="return_buyer_initial_page", size=9)]]
    return sg.Window('Sign-Up Page', layout, size=default_window_size, element_justification='c')

def buyer_signup_button(values):
    global window
    y=True
    while True:
        today = datetime.now()
        if values['buyer_ssn'] == '':
            sg.popup("Buyer SSN should not be empty")
            break
        elif not values['buyer_ssn'].isnumeric():
            sg.popup("Buyer SSN should be numeric!")
            break
        elif not len(str(values['buyer_ssn'])) == 11:
            sg.popup("Length of seller SSN should be 11")
            break
        elif values['buyer_password'] == '':
            sg.popup("Buyer Password should not be empty")
            break
        elif values['buyer_name'] == '':
            sg.popup("Buyer Name should not be empty")
            break
        elif values['buyer_name'].isnumeric():
            sg.popup("Buyer Name should not contain numeric values!")
            break
        elif values['buyer_surname'] == '':
            sg.popup("Buyer Surname should not be empty")
            break
        elif values['buyer_surname'].isnumeric():
            sg.popup("Buyer surName should not contain numeric values!")
            break
        elif y:
            try:
                birth_date = datetime.strptime(values['buyer_birth_date'], '%Y-%m-%d')
                if (today-birth_date).days < 0:
                    sg.popup("Birthday cannot be in the future")
                    break
                elif (today-birth_date).days < 6570:
                    sg.popup("An Buyer should be above 18 years old!")
                    break
            except:
                sg.popup("Buyer birthdate should not be empty")
                break
            y = False
        elif (today-birth_date).days < 0:
            sg.popup("Birthday cannot be in the future")
            break
        elif (today-birth_date).days < 6570:
            sg.popup("Buyer should be above 18 years old!")
            break
        else:
            unique_ssn = True
            cur.execute('SELECT buyerSSN FROM Buyer')
            row = cur.fetchall()
            for tuple_ in row:
                if int(values['buyer_ssn']) == tuple_[0]:
                    unique_ssn = False
                    break
            if not unique_ssn:
                sg.popup('This SSN is already in use.')
                break
            buyer_name = values['buyer_name']
            buyer_surname = values['buyer_surname']
            buyer_SSN = values['buyer_ssn']
            buyer_password = values['buyer_password']
            buyer_birthday = values['buyer_birth_date']
            cur.execute('''INSERT INTO Buyer VALUES (?,?,?,?,?)''', (buyer_SSN,
                    buyer_name, buyer_surname, buyer_password, buyer_birthday))
            sg.popup(f'Welcome to our app, {buyer_name}!')
            window.close()
            window = buyer_login_window()
            con.commit()
            break
        
def buyer_login_button(values):
    global login_SSN
    global window
    # get the seller ssn from the input
    b_ssn = values['buyer_ssn']
    b_password = values['buyer_password']

    # if no ssn is entered, give error message.
    if b_ssn == '':
        sg.popup('SSN cannot be empty!')
    elif b_password == '':
        sg.popup('Password cannot be empty!')

    # if a ssn and a password is entered, check if it is in the Seller table of the database.
    # if it is not in the Seller table, give error message.
    # if it is in the Seller table, proceed with the corresponding seller ssn.
    else:
        cur.execute(
            'SELECT buyerSSN FROM Buyer WHERE buyerSSN = ? AND BPassword = ?', (b_ssn, b_password))
        row = cur.fetchone()
        if row is None:
            sg.popup('Either ssn or password is wrong!')
        else:
            login_SSN = row[0]
            window.close()
            window = buyer_main_window()
            
def buyer_main_window():
    global window
    global auction_list
    auction_list = []
    for row in cur.execute("select * from Auction where status = 'Ongoing'"):
        auction_list.append([row[0],row[4],row[5],row[6],row[7],row[8],row[11]])
    layout = [[sg.Text('', size=(20, 4))],
              [sg.Button('Auctions:', size=(20, 1), key='auctions')],
              [sg.Button('Payment Information', key= 'Payment_Info', size=20)],
              [sg.Button('Won Auctions', key= 'won_auctions', size=20)],
              [sg.Button('Refresh',key= "refresh", size=20)],
              [sg.Button('Go Back', key="return_buyer_initial_page", size=20)],
              [sg.Button('Log Out', key='buyer_log_out', size=20)]]

    return sg.Window('Buyer main window', layout, size=default_window_size, element_justification='c') 
   
def Payment_Information_window():
    global window
    global payment_info
    payment_info = []
    buyer_SSN = login_SSN
    for row in  cur.execute(f'SELECT buyerSSN, CCnum FROM PaymentInfo Where buyerSSN = {buyer_SSN}'):
        payment_info.append((row[0], row[1]))
    layout = [[sg.Text('', size=(20, 4))],
              #[sg.Text('Current', size=(20, 1), key='Payment_Info')],
              [sg.Text('', size=(5,1)), sg.Text('Payment Info List:', size=(10,10)),
               sg.Listbox(payment_info, key= "Updated_payment_ınfo",size=(70, 10), select_mode='multiple')],
              [sg.Text('', size=(5,1)), sg.Text('', size=(10,1)), sg.Button('Update selected payments', key = 'Updated_payment_ınfo_window',  size=(35,1))],
              [sg.Button('Go Back', key='return_buyer_main_window', size=20)],
              [sg.Button('Log Out', key='buyer_log_out', size=20)]]
    return sg.Window('Payment Information Window', layout, size=default_window_size, element_justification='c')
   
def select_payment_button (values):
    global window
    global payment_info
    global selected_payment
    selected_payment = values["Updated_payment_ınfo"]
    while True:
        if selected_payment == []:
            sg.popup("You should select auctions to bid first!")
            break
        else:
            window.close()
            window = Payment_info_update(values)
            break

def Payment_info_update(values):
    global payment_info
    global selected_payment
    selected_payment = values["Updated_payment_ınfo"]
    payment_info = selected_payment

    layout2 = [[sg.Text(f'Buyer SSN: {payment_info[i][0]} Credit Card Number: {payment_info[i][1]}', size=(50,1)), sg.Input(key=f'payment_info{payment_info[i][1]}', size=(17,1)), sg.Text("."), sg.Button('Save', key = f'save_payment_button{i}',size =(17,1))]for i in range(len(payment_info))]
    layout3 = [[sg.Text('', size=(50,1)),sg.Button('Go Back', key="return_to_payment_info_window", size =(17,1)) ]]
    layout = [[layout2], [layout3]]
    return sg.Window('Set Payment info Window', layout, size=default_window_size)

def save_paymentinfo_button (values, item):
    global window
    global payment_info
    new_payment_info = values[f'payment_info{payment_info[item][1]}']
    current_payment_info= int(payment_info[item][1])
 
    while True:
        if new_payment_info == '' :
            sg.popup("Payment info should not be empty!")
            break
        
        elif not new_payment_info.isnumeric():
            sg.popup("Payment info should be numeric!")
            break
        elif current_payment_info == int(new_payment_info) :
            sg.popup("Payment info should be new!")
            break
        else:
            cur.execute('''Update PaymentInfo Set CCnum=? where buyerSSN=?''',(new_payment_info, login_SSN))
            con.commit()         
            sg.popup('Successfully updated!')
            break
def auction_window ():
    global window
    global auction_list
    auction_list = []
    
    for row in cur.execute("select * from Auction WHERE status = 'Ongoing' or status = 'Finished'"):
            auction_list.append([row[8],row[0],row[4],row[5],row[6],row[7],row[9]])
    layout = [[sg.Text('', size=(20, 4))],
              [sg.Text('Auctions:', size=(20, 1), key='auctions')],
              [sg.Text('', size=(5,1)), sg.Text('Auction List:', size=(10,10)),
               sg.Listbox(auction_list, key= "auctions_to_enter",size=(70, 10), select_mode='multiple')],
              [sg.Text('', size=(5,1)), sg.Text('', size=(10,1)), sg.Button('Bid selected auctions', key = 'selected_auction',  size=(35,1))],
              [sg.Button('Go Back', key='return_buyer_main_window', size=20)],
              [sg.Button('Log Out', key='buyer_log_out', size=20)]]
    return sg.Window('Ongoing auction window', layout, size=default_window_size, element_justification='c')

def select_auction_button (values):
    global window
    global auction_list
    global selected_auctions_bid
    y = True
    selected_auctions_bid = values["auctions_to_enter"]
    while y == True:
        if selected_auctions_bid == []:
            sg.popup("You should select auctions to bid first!")
            break
        elif selected_auctions_bid != []:
            for i in selected_auctions_bid:
                if i[0] != 'Ongoing':
                  sg.popup("You should select auctions that are ongoing to bid!")
                  y = False
                  window.close()
                  window = auction_window()
                  break
            break
    if y == True:
        window.close()
        window = bid_auction(values)
    else:
        window.close()
        window = auction_window()
    
    
def bid_auction(values):
    global auction_list
    auction_list = selected_auctions_bid
    layout2 = [[sg.Text(f'{auction_list[i][0]}{auction_list[i][3]} Bin Price:{auction_list[i][4]} CurrentP:{auction_list[i][5]} SPrice:{auction_list[i][6]}', size=(50,1)), sg.Text("$"), sg.Input(key=f'new_bid{auction_list[i][0]}', size=(6,1)), sg.Text("."), sg.Input(key=f'new_bid_dec{auction_list[i][0]}', size=(6,1)), sg.Button('Save', key = f'save_button{i}',size =(17,1)), sg.Button('Buy it now', key = f'bin_button{i}',size =(17,1)) ] for i in range(len(auction_list))]
    layout3 = [[sg.Text('', size=(50,1)),sg.Button('Go Back', key="return_to_auction_window", size =(17,1)) ]]
    layout = [[layout2], [layout3]]
    return sg.Window('Set Bid Window', layout, size=default_window_size)


def bin_button (values,item):
    global window
    global auction_list
    purchase_ID = []
    cur.execute('SELECT purchaseID FROM Winner')
    row = cur.fetchall()
    for aid in row:
        purchase_ID.append(aid[0])
    new_purchase_id = max(purchase_ID) + 1
    cur.execute('SELECT pID FROM PaymentInfo WHERE buyerSSN = ?', (login_SSN,))
    payment_method = int(cur.fetchone()[0])
    purchase_price = auction_list[item][4]
    auction_ID = auction_list[item][1]
    cur.execute('SELECT auID FROM Winner')
    ahmet = cur.fetchall()
    auIds = []
    for i in ahmet:
        auIds.append(i[0])
    print(auIds)
    if auction_ID in auIds:
        sg.popup("It is already bought!")
    else:
        cur.execute('INSERT INTO Winner VALUES (?,?,?,?,?) ', (new_purchase_id,login_SSN, payment_method, purchase_price, auction_ID))
        cur.execute("Update Auction Set status= 'Finished' where auID=?", (auction_ID,))
        con.commit()
        sg.popup("Congratulations! You are the winner.\nYou can complete your purchase now.")
        auIds.append (auction_ID)

    
def buyer_payment_window():
    global window
    payments = []
    buyer_SSN = login_SSN
    cur.execute(f'SELECT buyerSSN, CCnum FROM PaymentInfo Where buyerSSN = {buyer_SSN}')
    all_payments = cur.fetchall()
    for payment in all_payments:
        payments.append(payment)
    layout = [[sg.Text('', size=(20, 4))],
              [sg.Text('Current', size=(20, 1), key='payments')],
              [sg.Text('', size=(5,1)), sg.Text('Payment Info List:', size=(10,10)),
               sg.Listbox(payment_info, key= "selected_payment_buy",size=(70, 10))],
              [sg.Text('', size=(5,1)), sg.Text('', size=(10,1)), sg.Button('Bid select payment', key = 'purchase_auction',  size=(35,1))],
              [sg.Button('Go Back', key='return_auction_window', size=20)],
              [sg.Button('Log Out', key='buyer_log_out', size=20)]]
    return sg.Window('Select Payment Method', layout, size=default_window_size, element_justification='c')    
    
    
    
    
def save_bid_button (values, item):
    global window
    global auction_list
    t = True
    new_bid = values[f'new_bid{auction_list[item][0]}']
    new_bid_dec = values[f'new_bid_dec{auction_list[item][0]}']
    starting_price = int(auction_list[item][6])
    try:
        current_price = auction_list[item][5]
        current_price.isnumeric()
    except:
        current_price = starting_price
        cur.execute('''Update Auction Set currentPrice=? where auID=?''',(starting_price, auction_list[item][1]))
        con.commit()  
    while True:
        if new_bid == '' :
            sg.popup("New bid should not be empty!")
            break
        elif new_bid_dec == '' :
            sg.popup("New bid's decimal should not be empty!")
            break
        
        elif not new_bid.isnumeric():
            sg.popup("New bid should be numeric!")
            break
        elif not new_bid_dec.isnumeric():
            sg.popup("New bid's decimal should be numeric!")
            break
        elif t:
            new_bid_decimal_value = int(new_bid_dec) / (10**len(str(new_bid_dec)))
            last_price= int(new_bid) + new_bid_decimal_value
            current_price = auction_list[item][5]
            t = False
        
        elif last_price < current_price  :
            sg.popup("New bid should be greater than current price!")
            break
        
        else:
            sg.popup('Successfully bidded!')
            cur.execute('''Update Auction Set currentPrice=? where auID=?''',(last_price, auction_list[item][1]))
            con.commit()            
            break

def winned_auctions_window():
    global window
    winner_SSN = login_SSN
    global won_auction_list
    won_auction_list = []
    for row in cur.execute(f"select B.auID, B.title, B.description, B.PaymentStatus, A.purchasePrice from Winner A, Auction B WHERE A.winnerSSN = {winner_SSN} and A.auID = B.auID"):
        won_auction_list.append((row[0], row[1], row[2], row[3],row[4]))
    
    layout = [[sg.Text('', size=(20, 4))],
              [sg.Text('Auctions:', size=(20, 1), key='auctions')],
              [sg.Text('', size=(5,1)), sg.Text('Auction List:', size=(10,10)),
               sg.Listbox(won_auction_list, key= "winned_auctions",size=(70, 10), select_mode='multiple')],
              [sg.Text('', size=(5,1)), sg.Text('', size=(10,1)), sg.Button('Pay selected auctions', key = 'to_be_paid_auctions',  size=(35,1))],
              [sg.Button('Go Back', key='return_buyer_main_window', size=20)],
              [sg.Button('Log Out', key='buyer_log_out', size=20)]]
    return sg.Window('Winned Auctions', layout, size=default_window_size, element_justification='c')

def winner_payment_information_window():
    global window
    global payment_info
    payment_info = []
    buyer_SSN = login_SSN
    for row in  cur.execute(f'SELECT buyerSSN, CCnum FROM PaymentInfo Where buyerSSN = {buyer_SSN}'):
        payment_info.append((row[0], row[1]))
    layout = [[sg.Text('', size=(20, 4))],
              #[sg.Text('Current', size=(20, 1), key='Payment_Info')],
              [sg.Text('', size=(5,1)), sg.Text('Payment Info List:', size=(10,10)),
               sg.Listbox(payment_info, key= "payment_methods_of_winner",size=(70, 10), select_mode='single')],
              [sg.Button('Pay', key='pay_unpaid_auction', size=20)],
              [sg.Button('Go Back', key='return_buyer_main_window', size=20)],
              [sg.Button('Log Out', key='buyer_log_out', size=20)]]
    return sg.Window('Payment Selection Window', layout, size=default_window_size, element_justification='c')
   

def pay_button(values):
    global window
    global won_auction_list
    winner_SSN = login_SSN
    won_auction = []
    payment_method = []
    transNums = []
    winned_auctions = won_auction_list
    payment_method_winner = values['payment_methods_of_winner']
    for i in winned_auctions:
        won_auction.append(i[0])
    payment_method.append(payment_method_winner[0])
    for a in won_auction:
        cur.execute('''Update Auction Set PaymentStatus=? where auID=?''',("Paid",a))
        con.commit()
    for item in winned_auctions:
        cur.execute('SELECT transNum FROM Bill')
        row = cur.fetchall()
        for trans in row:
            transNums.append(trans[0])
        new_trans_id = max(transNums) + 1
        cur.execute('SELECT sellerSSN FROM Auction WHERE auID = ?', (item[0],))
        sellerSSN = int(cur.fetchone()[0])
        cur.execute("Insert Into Bill VALUES (?,?,?,?)", (new_trans_id, item[4], sellerSSN, winner_SSN ))
        con.commit()
    sg.popup('Paid!')
    
def admin_initial_window():
    
    global window
    
    layout =[[sg.Text('', size=(20,4))],
              [sg.Button('Login', key= "admin_login", size=20)],
              [sg.Button('Sign UP',key= "admin_signup", size=20)],
              
              [sg.Button('Back to Main Menu', size=20)],
              [sg.Exit(size=(20))]]
    return sg.Window('Admin initial window', layout, size=default_window_size, element_justification='c')  

def admin_login_button(values):
    
    global login_SSN
    global window    
    
    s_ssn = values['admin_ssn']
    s_password = values['admin_password']
    
    if s_ssn == '':
        sg.popup('SSN cannot be empty!')
    elif s_password == '':
        sg.popup('Password cannot be empty!')
    else:
        cur.execute('SELECT adminSSN FROM Admin WHERE adminSSN = ? AND Apassword = ?', (s_ssn, s_password))
        row = cur.fetchone()
        if row is None:
            sg.popup('Either ssn or password is wrong!')
        else:
            login_SSN = row[0]
            window.close()
            window = admin_main_window()        
            
def admin_login_window() :
    layout=[[sg.Text('', size=(20,4))],
              [sg.Text('SSN', size=20),sg.Input(key='admin_ssn', size=30)],
              [sg.Text('password', size=20),sg.Input(key='admin_password', size=30)],
              [sg.Button('Sign in', key='admin_sign_in', size=20)],
              [sg.Button('Go Back', key="return_admin_initial_page", size=20)],
              [sg.Exit(size=(20))]]
    return sg.Window('Admin login window', layout, size=default_window_size, element_justification='c')

def admin_main_window():
    global window
    auctions = []
    admin_SSN = login_SSN
    cur.execute(f'SELECT * FROM Auction Where adminSSN = {admin_SSN} and (status = "Ongoing" or status = "NotAccepted")')
    all_auctions = cur.fetchall()
    for auction in all_auctions:
        auctions.append(auction)
    layout = [[sg.Text('', size=(25,2))],
               [sg.Text('Auctions:', size=(10,10)),
                sg.Combo(auctions,key="auctions",size=(60, 10))],
               [sg.Text('', size=(10,1)), sg.Button('Accept Auction',key = "accept_auction", size=30)],
               [sg.Text('', size=(10,1)), sg.Button('Commission',key = "commission_auction", size=30)],
               [sg.Button('Refresh',key= "refresh", size=20)],
               [sg.Text('', size=(10,1)), sg.Button('Log out',key = 'Back to Main Menu', size=30)]] 
    return sg.Window('Auction page', layout, size=default_window_size, element_justification='c')

def accept_auction_button(values):
    global window
    global auID
    while True: 
        if values["auctions"] == '':
            sg.popup("An auction should be chosen for this function")
            break
        elif values["auctions"][8] != 'NotAccepted':
            sg.popup("Chosen auction's status should be -Not Accepted- for this function")
            break
        else:
            sg.popup("Chosen auction is accepted")
            cur.execute('''Update Auction Set status=? where auID=?''',("Ongoing",values["auctions"][0]))
            con.commit()            
            window.close()
            window = admin_main_window()
            break

def admin_signup_window():
    layout = [[sg.Text('', size=(25, 4))],
              [sg.Text('', size=(5, 1)), sg.Text('SSN', size=(22, 1)),
               sg.Input(key='admin_signup_ssn', size=30)],
              [sg.Text('', size=(5, 1)), sg.Text('Password', size=(
                  22, 1)), sg.Input(key='admin_password', size=30)],
    
              [sg.Text('', size=(5, 1)), sg.Text('Name', size=(22, 1)),
               sg.Input(key='admin_name', size=30)],
              [sg.Text('', size=(5, 1)), sg.Text('Surname', size=(22, 1)),
               sg.Input(key='admin_surname', size=30)],
              [sg.Text('', size=(5, 1)), sg.Text('Birth', size=(22, 1)), sg.Input(
                  key='admin_birth_date', size=(15, 1)), sg.CalendarButton('Choose Date', format='%Y-%m-%d')],
              [sg.Text('', size=(5, 1)), sg.Text('', size=(22, 1)), sg.Button(
                  'Sign-Up', key="admin_signup_button", size=9, bind_return_key=True)],
              [sg.Text('', size=(5, 1)), sg.Text('', size=(22, 1)), sg.Button(
                  'Go Back', key="return_admin_initial_page", size=9)],
              [sg.Exit(size=(25))]]
    return sg.Window('Admin Sign-Up Page', layout, size=default_window_size, element_justification='c')

def admin_signup_button(values):

    global window
    z=True
    while True:
        today = datetime.now()
        if values['admin_signup_ssn'] == '':
            sg.popup("Admin SSN should not be empty")
            break
        elif not values['admin_signup_ssn'].isnumeric():
            sg.popup("Admin SSN should be numeric!")
            break
        elif not len(str(values['admin_signup_ssn'])) == 11:
            sg.popup("Length of admin SSN should be 11")
            break
        elif values['admin_password'] == '':
            sg.popup("Admin Password should not be empty")
            break
        
        elif values['admin_name'] == '':
            sg.popup("Admin Name should not be empty")
            break
        elif values['admin_surname'] == '':
            sg.popup("Admin Surname should not be empty")
            break
        elif values['admin_name'].isnumeric():
            sg.popup("Admin Name should not contain numeric values!")
            break
        elif values['admin_surname'].isnumeric():
            sg.popup("Admin surName should not contain numeric values!")
            break
        elif values['admin_birth_date'] == '':
            sg.popup("Admin Birthday should not be empty")
            break
        elif z:
            try:
                birth_date = datetime.strptime(values['admin_birth_date'], '%Y-%m-%d')
                if (today-birth_date).days < 0:
                    sg.popup("Birthday cannot be in the future")
                    break
                elif (today-birth_date).days < 6570:
                    sg.popup("An Admin should be above 18 years old!")
                    break
            except:
                sg.popup("Admin birthdate should not be empty")
                break
            z = False
        elif (today-birth_date).days < 0:
            sg.popup("Birthday cannot be in the future")
            break
        elif (today-birth_date).days < 6570:
            sg.popup("Admin should be above 18 years old!")
            break
        else:
            unique_ssn = True
            cur.execute('SELECT adminSSN FROM Admin')
            row = cur.fetchall()
            for tuple_ in row:
                print(tuple_)
                if int(values['admin_signup_ssn']) == tuple_[0]:
                    unique_ssn = False
                    break
            if not unique_ssn:
                sg.popup('This SSN is already in use.')
                break
            admin_name = values['admin_name']
            admin_surname = values['admin_surname']
            admin_SSN = values['admin_signup_ssn']
            admin_password = values['admin_password']
            admin_birthday = values['admin_birth_date']
            cur.execute('''INSERT INTO Admin VALUES (?,?,?,?,?)''', (admin_SSN,
                    admin_name, admin_surname, admin_password, admin_birthday))
            sg.popup(f'Welcome to our app, {admin_name}!')
            window.close()
            window = admin_login_window()
            con.commit()
            break

def admin_commission_window(values):
    global window
    global finished_auction_list
    
    finished_auction_list = []
    
    
    for row in cur.execute("Select a.auID,a.title,w.winnerSSN,a.SellerSSN, w.purchasePrice*0.2  From Winner w, Bid b, Auction a WHERE  a.status= 'Finished' and w.winnerSSN=b.buyerSSN and b.auID=a.auID and w.auID=a.auID and a.adminSSN=?",(login_SSN,)):
        finished_auction_list.append((row[0],row[1],row[2],row[3],"Commission:",row[4]))
        print(finished_auction_list)
    layout = [[sg.Text('', size=(20, 4))],
              [sg.Text('Auctions:', size=(20, 1), key='auctions')],
              [sg.Text('', size=(5,1)), sg.Text('Auction List:', size=(10,10)),
               sg.Listbox(finished_auction_list, key= "auctions_for_commission",size=(70, 10))],
              
              [sg.Button('Go Back', key='return_admin_main_window', size=20)],
              [sg.Button('Log Out', key='admin_log_out', size=20)]]
    return sg.Window('Finished auction window', layout, size=default_window_size, element_justification='c')
def refresh_button(values):
    global window
    purchase_ID = []
    refresh_auction =[]
    auid_list = []
    cur.execute("SELECT auID FROM Winner")
    row2 = cur.fetchall()
    for i in row2:
        auid_list.append(i[0])
    
    cur.execute('SELECT purchaseID FROM Winner')
    row = cur.fetchall()
    for aid in row:
        purchase_ID.append(aid[0])
    new_purchase_id = max(purchase_ID) + 1
    
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cur.execute("UPDATE Auction SET status = ? WHERE eDate <= ? and status = ?", ("Finished", current_time,"Ongoing"))
    cur.execute("SELECT * FROM Auction WHERE eDate <= ? and status = ?", (current_time,"Ongoing"))
    row = cur.fetchall()
    for item in row:
        refresh_auction.append(row[0],row[7])
    
    cur.execute("SELECT max(bidPrice), auID, buyerSSN From Bid group by auID ")
    row1 = cur.fetchall()
    for item in row1:
        refresh_auction.append((item[0], item[1], item[2]))
    
    for item in refresh_auction:
        if item[1] not in auid_list:
            
            cur.execute ('SELECT pID from PaymentInfo WHERE buyerSSN = ?', (item[2],))
            payment_method = int(cur.fetchone()[0])
            cur.execute('SELECT purchaseID FROM Winner')
            row = cur.fetchall()
            for aid in row:
                purchase_ID.append(aid[0])
            new_purchase_id = max(purchase_ID) + 1
            cur.execute("INSERT INTO Winner Values(?,?,?,?,?)", (new_purchase_id, item[2], payment_method, item[0], item[1]))
            con.commit()
    sg.popup("Updated!")
    


window = initial_window()
while running:
    event, values = window.read()
    # PHASE1 WINDOWS
    for item in range(len(auction_list)):
        if event == f'save_button{item}':
            save_bid_button(values, item)
    for item in range(len(payment_info)):
        if event == f'save_payment_button{item}':
            save_paymentinfo_button(values, item)       
    if event == 'Buyer':
        window.close()
        window = buyer_initial_window()
    elif event == 'Seller':
        window.close()
        window = seller_initial_window()
    elif event == 'Admin':
        window.close()
        window = admin_initial_window()
    #PHASE2 WINDOWS (admin sign up)
    elif event == 'admin_signup':
        window.close()
        window = admin_signup_window()
    elif event == 'admin_signup_button':
        admin_signup_button(values)
    # PHASE2 WINDOWS (seller sign up)
    elif event == 'seller_signup':
        window.close()
        window = seller_signup_window()
    elif event == 'seller_signup_button':
        seller_signup_button(values)
    # PHASE2 WINDOWS (seller log in)
    elif event == 'seller_login':
        window.close()
        window = seller_login_window()
    #PHASE2 WINDOWS (admin login)
    elif event=='admin_login':
         window.close()
         window=admin_login_window()
    # PHASE2 WINDOWS (buyer sign up)
    
    elif event == "buyer_signup":
        window.close()
        window = buyer_signup_window()
    elif event == 'buyer_signup_button':
        buyer_signup_button(values)
    # PHASE2 WINDOWS (buyer log in)
    elif event == 'buyer_login':
        window.close()
        window = buyer_login_window()
    # PHASE2 WINDOWS (common)
    elif event == 'Back to Main Menu':
        window.close()
        window = initial_window()
    # PHASE3 WINDOWS (seller)
    elif event == 'seller_login_button':
        seller_login_button(values)
    elif event == 'return_seller_initial_page':
        window.close()
        window = seller_initial_window()
    #PHASE 3(admin sign in)
    elif event== 'admin_sign_in':
         admin_login_button(values)
    # PHASE3 WINDOWS (buyer)
    elif event == 'buyer_login_button':
        buyer_login_button(values)
    elif event == 'return_buyer_initial_page':
        window.close()
        window = buyer_initial_window()
    # PHASE4 WINDOWS (seller auction)
    elif event == 'new_auction':
        window.close()
        window = new_auction_window()
    elif event == "my_auctions":
        window.close()
        window = active_auction_window()
    # PHASE5 WINDOWS (S)
    elif event == 'bid_list' :
        list_bids_button(values)
    elif event == 'save_new_auction':
        seller_save_button(values)
    elif event == 'check_bill':
        check_bill_button(values)
    elif event == "delete_auction":
        delete_auction_button(values)
    elif event == 'seller_log_out':
        window.close()
        window = seller_initial_window()
    elif event == 'buyer_log_out':
        window.close()
        window = buyer_initial_window()
    elif event == 'admin_log_out':
        window.close()
        window = admin_initial_window()
    elif event == 'return_admin_main_window':
        window.close()
        window = admin_main_window()
    elif event == 'return_buyer_main_window':
        window.close()
        window = buyer_main_window()
    elif event == 'selected_auction':
        select_auction_button (values)
    elif event == 'return_seller_main_page':
        window.close()
        window = seller_main_window()
    elif event == 'return_to_auction_window':
        window.close()
        window = auction_window()
    elif event == 'Payment_Info':
        window.close()
        window = Payment_Information_window()
    elif event == 'auctions':
        window.close()
        window = auction_window()
    elif event == 'Updated_payment_ınfo_window':
        window.close()
        window = Payment_info_update(values)
    elif event == "return_to_payment_info_window":
        window.close()
        window =  Payment_Information_window() 
    elif event == 'refresh':
        refresh_button(values)
        #ADMIN ACCEPTING AUCTION
    elif event == 'accept_auction':
        accept_auction_button(values)
    elif event == "return_admin_initial_page":
        window.close()
        window = admin_initial_window()
    elif event=="commission_auction":
        window.close()
        window = admin_commission_window(values)
    elif event == "won_auctions":
        window.close()
        window = winned_auctions_window()
    elif event == "to_be_paid_auctions":
        window.close()
        window = winner_payment_information_window()
    elif event == "pay_unpaid_auction":
        pay_button(values)
    
    # Closing statements"
    elif event == sg.WIN_CLOSED:
        running = False
    elif event == 'Exit':
        running = False


con.commit()
window.close()
