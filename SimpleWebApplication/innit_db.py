from __init__ import db, Foods

db.drop_all()
db.create_all()

f1 = Foods(img = "https://littlecaesarsdelivery.sg/wp-content/uploads/2021/01/Pepperoni.png",
           name = "Pizza",
           price = 16,
           description="Pizzabro")

f2 = Foods(img = "https://food.fnr.sndimg.com/content/dam/images/food/fullset/2004/2/25/0/bw2b07_hambugers1.jpg.rend.hgtvcom.616.462.suffix/1558017418187.jpeg",
           name = "Burger",
           price = 12,
           description="bunger")

f3 = Foods(img = "https://www.bestvaluemart.com.sg/4766-superlarge_default/coca-cola-coke-original-can-320ml-soft-drinks-parties-gathering-bbq.jpg",
           name = "Coke",
           price = 2,
           description="Drimnk")

f4 = Foods(img = "https://static.onecms.io/wp-content/uploads/sites/43/2022/08/08/50223-homemade-crispy-seasoned-french-fries-ddmfs-4x3-0721.jpg",
           name = "Fries",
           price = 5,
           description="S a l t")

f5 = Foods(img = "https://masalaandchai.com/wp-content/uploads/2022/03/Butter-Chicken-500x500.jpg",
           name = "Butter chicken",
           price = 15,
           description="Chimioncn")

f6 = Foods(img = "https://www.errenskitchen.com/wp-content/uploads/2015/02/Quick-Easy-Spaghetti-Bolognese2-1-500x480.jpg",
           name = "Spaghetti",
           price = 10.50,
           description="pasghetti")

f7 = Foods(img = "https://www.aiyoevent.com.sg/wp-content/uploads/2023/02/roti-prata.jpg",
           name = "Prata",
           price = 13.20,
           description="prata")

f8 = Foods(img = "https://cdn.discordapp.com/attachments/1068170472946151525/1073648477462081546/IMG_1399.jpg",
           name = "Benjamin",
           price = 1.00,
           description="Slave")

db.session.add_all([f1, f2, f3, f4, f5, f6, f7, f8])

db.session.commit()