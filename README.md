# delivery_app

## Made necessary tables
# Create database
# 1. Users
#   All User basic info
# Id      First Name    Last Name      Email                             Phone         Username         Password
# UR1024  Niranjan      Vishnubhatla   niranjan.vishnubhatla@gmail.com   9876543210    vnda vision      vnda vision
#   All their orders
# o_Id     Order Number       Item              Qunatity   price      Delivered time
# UR1024 OR3241         Iphone 15             1          150000     date and time
# 2. Vendors
#   All their info
# v_Id      Name              Phone       Email                      latitude  longitude   City        State     Country     Password
# VR1024  Rahul Donthula    9876543210  rahul.donthula@gmail.com   72.9876   17.7653     Hyderabad   Telangana India       rahul donthula
#   All their item list
# va_Id     Item Number  Item         Quantity  Price
# VR1024 IN1024       Iphone 15    10        150000  
# 3. Admin  
#   The order list that are pending
# Order Id      Driver     Delivery Time
# UR1024OR3241  DV1059     date and time
# 4. Driver
#   The driver info
# d_Id        Name           License         PAN         Aadhar         Home        Phone
# DV1059   Sohith          LC1234          PFDGH1234Q  1234567890    alwal        9876543210
#   The driver availability
# da_Id     Location           Free after time
# DV1059 alwal              date time model

