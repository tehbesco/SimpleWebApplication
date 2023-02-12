from __init__ import db, Foods

db.drop_all()
db.create_all()

f1 = Foods(img = "https://littlecaesarsdelivery.sg/wp-content/uploads/2021/01/Pepperoni.png",
           name = "Pizza",
           price = 16,
           tags="Western",
           restaurant="Pizzahut")

f2 = Foods(img = "https://food.fnr.sndimg.com/content/dam/images/food/fullset/2004/2/25/0/bw2b07_hambugers1.jpg.rend.hgtvcom.616.462.suffix/1558017418187.jpeg",
           name = "Burger",
           price = 12,
           tags="Western",
           restaurant="Burgerking")

f3 = Foods(img = "https://www.bestvaluemart.com.sg/4766-superlarge_default/coca-cola-coke-original-can-320ml-soft-drinks-parties-gathering-bbq.jpg",
           name = "Coke",
           price = 2,
           tags="Drinks",
           restaurant="Mcdonalds")

f4 = Foods(img = "https://static.onecms.io/wp-content/uploads/sites/43/2022/08/08/50223-homemade-crispy-seasoned-french-fries-ddmfs-4x3-0721.jpg",
           name = "Fries",
           price = 5,
           tags="Western",
           restaurant="Mcdonalds")

f5 = Foods(img = "https://masalaandchai.com/wp-content/uploads/2022/03/Butter-Chicken-500x500.jpg",
           name = "Butter chicken",
           price = 15,
           tags="Indian",
           restaurant="Syed shop")

f6 = Foods(img = "https://www.errenskitchen.com/wp-content/uploads/2015/02/Quick-Easy-Spaghetti-Bolognese2-1-500x480.jpg",
           name = "Spaghetti",
           price = 10.50,
           tags="Western",
           restaurant="Jolibee")

f7 = Foods(img = "https://www.aiyoevent.com.sg/wp-content/uploads/2023/02/roti-prata.jpg",
           name = "Prata",
           price = 13.20,
           tags="Indian",
           restaurant="Syed shop")

f8 = Foods(img = "https://cdn.discordapp.com/attachments/1068170472946151525/1073648477462081546/IMG_1399.jpg",
           name = "Benjamin",
           price = 1.00,
           tags="Slave",
           restaurant="Benjamin slave labour")

f9 = Foods(img = "https://littlecaesarsdelivery.sg/wp-content/uploads/2021/01/Pepperoni.png",
           name = "Pizza",
           price = 16,
           tags="Western",
           restaurant="Little Caesar's")

f10 = Foods(img = "https://food.fnr.sndimg.com/content/dam/images/food/fullset/2004/2/25/0/bw2b07_hambugers1.jpg.rend.hgtvcom.616.462.suffix/1558017418187.jpeg",
           name = "Burger",
           price = 12,
           tags="Western",
           restaurant="Mcdonalds")

f11 = Foods(img = "https://www.pokka.co/images/default-source/partner-brands/pepsi-08--pepsi-black-320ml.jpg?sfvrsn=485f9013_4",
           name = "Pepsi",
           price = 2,
           tags="Drinks",
           restaurant="Burger King")

f12 = Foods(img = "https://static.onecms.io/wp-content/uploads/sites/43/2022/08/08/50223-homemade-crispy-seasoned-french-fries-ddmfs-4x3-0721.jpg",
           name = "Fries",
           price = 5,
           tags="Western",
           restaurant="Burger King")

f13 = Foods(img = "https://whattocooktoday.com/wp-content/uploads/2018/09/konlo-mee-3-500x500.jpg",
           name = "Wonton noodles",
           price = 5,
           tags="Chinese",
           restaurant="Cho Kee Noodle")

f14 = Foods(img = "https://www.wandercooks.com/wp-content/uploads/2020/12/japanese-gyoza-dumplings-recipe-6-500x500.jpg",
           name = "Gyoza",
           price = 6.50,
           tags="Japanese",
           restaurant="Sukiyaki")

f15 = Foods(img = "https://www.jessicagavin.com/wp-content/uploads/2018/09/fried-rice-8-1200.jpg",
           name = "Fried Rice",
           price = 13.20,
           tags="Chinese",
           restaurant="Wok Hey")

f16 = Foods(img = "https://www.insidetherustickitchen.com/wp-content/uploads/2020/07/Quattro-formaggi-pizza-square-Inside-the-rustic-kitchen.jpg",
           name = "Cheese Pizza",
           price = 12.50,
           tags="Western",
           restaurant="Pizzahut")

db.session.add_all([f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12, f13, f14, f15, f16])

db.session.commit()
