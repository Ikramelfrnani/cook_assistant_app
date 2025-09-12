import customtkinter
from PIL import Image
from pymongo import MongoClient
from tkinter import messagebox
from tkinter import StringVar, IntVar

customtkinter.set_appearance_mode('light')
app = customtkinter.CTk()
app.geometry("1300x700")
app.title("Cook Assistant")
app.resizable(False, False)

cnx=MongoClient(host="localhost",port=27017)
db=cnx.dbCookAssistant

def Home(usernm):
    nameUs=usernm
    for widget in app.winfo_children():
        widget.destroy()

    def Delete(recipe_name):
        user = db.User.find_one({"username": nameUs}, {"saved_recipes": 1, "_id": 0})
        saved = user.get("saved_recipes", [])

        if recipe_name in saved:
            saved.remove(recipe_name)
            db.User.update_one({"username": nameUs}, {"$set": {"saved_recipes": saved}})
            messagebox.showinfo("Deleted", f"'{recipe_name}' has been removed from your saved recipes.")
            SavedRecipes(nameUs)

    def SavedRecipes(name):
        for widget in app.winfo_children():
            widget.destroy()

        mainframe = customtkinter.CTkFrame(app, fg_color="#fdfbd8")
        mainframe.pack(fill="both", expand=True)

        sidebar_frame = customtkinter.CTkFrame(master=mainframe, fg_color="white", width=176, height=650,
                                               corner_radius=20)
        sidebar_frame.pack_propagate(0)
        sidebar_frame.pack(fill="y", anchor="w", side="left")

        logo_img = customtkinter.CTkImage(Image.open("logo.png"), size=(77.68, 85.42))
        customtkinter.CTkLabel(master=sidebar_frame, text="", image=logo_img).pack(pady=(38, 0), anchor="center")
        myfont = customtkinter.CTkFont(family="Arial", size=16, weight="bold")
        icon_dash = customtkinter.CTkImage(Image.open("dashboard.png"), size=(15, 15))
        customtkinter.CTkButton(master=sidebar_frame, image=icon_dash, text="Dashboard", fg_color="transparent",
                                text_color="black", font=myfont, hover_color="#fffdd1", command=lambda: Home(usernm),
                                anchor="w").pack(anchor="center", ipady=5, padx=25, pady=(40, 0))
        icon_rec = customtkinter.CTkImage(Image.open("recipe.png"), size=(16, 16))
        customtkinter.CTkButton(master=sidebar_frame, image=icon_rec, text="All Recipes", fg_color="transparent",
                                text_color="black", font=myfont, hover_color="#fffdd1", command=AllRecipes,
                                anchor="w").pack(anchor="center", ipady=5, padx=25, pady=(15, 0))
        icon_fv = customtkinter.CTkImage(Image.open("favorite.png"), size=(18, 18))
        customtkinter.CTkButton(master=sidebar_frame, image=icon_fv, text="Saved", fg_color="transparent",
                                text_color="black", font=myfont, hover_color="#fffdd1",command=lambda: SavedRecipes(nameUs), anchor="w").pack(
            anchor="center", ipady=5, padx=25, pady=(15, 0))
        icon_st = customtkinter.CTkImage(Image.open("settings.png"), size=(18, 18))
        customtkinter.CTkButton(master=sidebar_frame, image=icon_st, text="Settings", fg_color="transparent",
                                text_color="black", font=myfont, hover_color="#fffdd1", anchor="w").pack(
            anchor="center", ipady=5, padx=25, pady=(300, 0))

        customtkinter.CTkLabel(master=mainframe, text="Your Saved Recipes", text_color="black",
                               font=("Arial", 20, "bold")).pack(pady=(38, 0), padx=60, anchor="w")

        recp=db.User.find_one({"username":name},{"saved_recipes":1,"_id":0})
        saverec = recp.get("saved_recipes", [])


        bigframe = customtkinter.CTkFrame(master=mainframe, fg_color="#fdfbd8", width=1300, height=700)
        bigframe.place(x=200, y=70)
        n = 40
        m = 30
        num = 0



        for i in range(len(saverec)):

            savedrecipes = db.Recipes.find({'name': saverec[i]},{"_id":0})
            nomRc=saverec[i]

            for elt in savedrecipes:
                card = customtkinter.CTkFrame(master=bigframe, fg_color="white", width=235, height=290)
                card.place(x=n, y=m)
                n = n + 255
                num = num + 1
                if (num == 4):
                    m = m + 300
                    n = 40
                    num = 0

                photo = customtkinter.CTkImage(Image.open(elt['image']), size=(240, 140))
                customtkinter.CTkLabel(master=card, text="", image=photo).place(x=0, y=0)
                customtkinter.CTkLabel(master=card, text=elt['rating'], font=("Arial", 12), text_color="#6D1E16").place(
                    x=15, y=150)
                btnDl = customtkinter.CTkButton(master=card, text="unsave", corner_radius=32, fg_color="#6D1E16",
                                                hover_color="#5B1613", width=40,
                                                font=("Arial", 13), text_color='white',command=lambda elt=elt: Delete(nomRc))


                btnDl.place(x=160, y=150)
                customtkinter.CTkLabel(master=card, text=elt['name'], font=("Arial", 16, "bold"),
                                       text_color="black").place(
                    x=15, y=175)
                btn = customtkinter.CTkButton(master=card, text="view recipe", corner_radius=32, fg_color="#6D1E16",
                                              hover_color="#5B1613",
                                              font=("Arial", 13), text_color='white', width=180,
                                              command=lambda elt=elt: ViewRecipe(elt['name']))
                btn.place(x=27, y=240)
                timer = customtkinter.CTkImage(Image.open("timer.png"), size=(14, 14))
                customtkinter.CTkLabel(master=card, text="", image=timer).place(x=16, y=200)
                chef = customtkinter.CTkImage(Image.open("chefhat.png"), size=(15, 15))
                customtkinter.CTkLabel(master=card, text="", image=chef).place(x=104, y=200)
                person = customtkinter.CTkImage(Image.open("person.png"), size=(16, 16))
                customtkinter.CTkLabel(master=card, text="", image=person).place(x=60, y=200)
                customtkinter.CTkLabel(master=card, text=elt['duration'], font=("Arial", 12),
                                       text_color="#B6B5B5").place(
                    x=38, y=200)
                customtkinter.CTkLabel(master=card, text=elt['people'], font=("Arial", 12), text_color="#B6B5B5").place(
                    x=82, y=200)
                customtkinter.CTkLabel(master=card, text=elt['level'], font=("Arial", 12), text_color="#B6B5B5").place(
                    x=126, y=200)





    def AllRecipes():
        for widget in app.winfo_children():
            widget.destroy()

        mainframe = customtkinter.CTkFrame(app, fg_color="#fdfbd8")
        mainframe.pack(fill="both", expand=True)

        sidebar_frame = customtkinter.CTkFrame(master=mainframe, fg_color="white", width=176, height=650,
                                               corner_radius=20)
        sidebar_frame.pack_propagate(0)
        sidebar_frame.pack(fill="y", anchor="w", side="left")

        logo_img = customtkinter.CTkImage(Image.open("logo.png"), size=(77.68, 85.42))
        customtkinter.CTkLabel(master=sidebar_frame, text="", image=logo_img).pack(pady=(38, 0), anchor="center")
        myfont = customtkinter.CTkFont(family="Arial", size=16, weight="bold")
        icon_dash = customtkinter.CTkImage(Image.open("dashboard.png"), size=(15, 15))
        customtkinter.CTkButton(master=sidebar_frame, image=icon_dash, text="Dashboard", fg_color="transparent",
                                text_color="black", font=myfont, hover_color="#fffdd1", command=lambda: Home(usernm),
                                anchor="w").pack(anchor="center", ipady=5, padx=25, pady=(40, 0))
        icon_rec = customtkinter.CTkImage(Image.open("recipe.png"), size=(16, 16))
        customtkinter.CTkButton(master=sidebar_frame, image=icon_rec, text="All Recipes", fg_color="transparent",
                                text_color="black", font=myfont, hover_color="#fffdd1", command=AllRecipes,
                                anchor="w").pack(anchor="center", ipady=5, padx=25, pady=(15, 0))
        icon_fv = customtkinter.CTkImage(Image.open("favorite.png"), size=(18, 18))
        customtkinter.CTkButton(master=sidebar_frame, image=icon_fv, text="Saved", fg_color="transparent",
                                text_color="black", font=myfont, hover_color="#fffdd1",command=lambda: SavedRecipes(nameUs), anchor="w").pack(
            anchor="center", ipady=5, padx=25, pady=(15, 0))
        icon_st = customtkinter.CTkImage(Image.open("settings.png"), size=(18, 18))
        customtkinter.CTkButton(master=sidebar_frame, image=icon_st, text="Settings", fg_color="transparent",
                                text_color="black", font=myfont, hover_color="#fffdd1", anchor="w").pack(
            anchor="center", ipady=5, padx=25, pady=(300, 0))

        customtkinter.CTkLabel(master=mainframe, text="All Recipes", text_color="black",
                               font=("Arial", 20, "bold")).pack(pady=(38, 0), padx=60, anchor="w")

        collection = db['Recipes']
        cuisine_types = collection.distinct("cuisine_type")
        cuisine_types.insert(0, "Cuisine Type")
        bycuisine = customtkinter.CTkComboBox(master=mainframe, values=cuisine_types, width=150, height=30, corner_radius=15,
                                              bg_color="#fdfbd8", fg_color="#fdfbd8", border_color="grey", border_width=1)
        bycuisine.place(x=1100,y=40)

        tastes = collection.distinct("taste")
        tastes.insert(0, "Taste")
        bytaste = customtkinter.CTkComboBox(master=mainframe, values=tastes, width=150, height=30,
                                              corner_radius=15,
                                              bg_color="#fdfbd8", fg_color="#fdfbd8", border_color="grey",
                                              border_width=1)
        bytaste.place(x=930, y=40)

        levels = collection.distinct("level")
        levels.insert(0, "Level")
        bylevel = customtkinter.CTkComboBox(master=mainframe, values=levels, width=150, height=30,
                                            corner_radius=15,
                                            bg_color="#fdfbd8", fg_color="#fdfbd8", border_color="grey",
                                            border_width=1)
        bylevel.place(x=760, y=40)

        recipes = db.Recipes.find({},{"_id": 0, "name": 1, 'duration': 1, 'people': 1, "image": 1, "level": 1,
                                   "rating": 1})

        def Saved(nom, usernm):
            donne = db.User.find_one({"username": usernm}, {"saved_recipes": 1, "_id": 0})
            exp = donne.get("saved_recipes", [])
            if nom not in exp:
                exp.append(nom)
            db.User.update_one({"username": usernm}, {"$set": {"saved_recipes": exp}})
            messagebox.showinfo("Saved", f"'{nom}' has been added to your saved recipes!")

        n = 40
        m = 30
        num = 0
        bigframe = customtkinter.CTkFrame(master=mainframe, fg_color="#fdfbd8", width=1300, height=700)
        bigframe.place(x=200, y=70)
        for elt in recipes:
            card = customtkinter.CTkFrame(master=bigframe, fg_color="white", width=235, height=290)
            card.place(x=n, y=m)
            n = n + 255
            num = num + 1
            if (num == 4):
                m = m + 300
                n = 40
                num = 0

            photo = customtkinter.CTkImage(Image.open(elt['image']), size=(240, 140))
            customtkinter.CTkLabel(master=card, text="", image=photo).place(x=0, y=0)
            customtkinter.CTkLabel(master=card, text=elt['rating'], font=("Arial", 12), text_color="#6D1E16").place(
                x=15, y=150)
            btnSave = customtkinter.CTkButton(master=card, text="save", corner_radius=32, fg_color="#6D1E16",
                                              hover_color="#5B1613", width=40,
                                              font=("Arial", 13), text_color='white',command=lambda elt=elt: Saved(elt['name'],nameUs)
                                              )
            btnSave.place(x=160, y=150)
            customtkinter.CTkLabel(master=card, text=elt['name'], font=("Arial", 16, "bold"),
                                   text_color="black").place(
                x=15, y=175)
            btn = customtkinter.CTkButton(master=card, text="view recipe", corner_radius=32, fg_color="#6D1E16",
                                          hover_color="#5B1613",
                                          font=("Arial", 13), text_color='white', width=180,
                                          command=lambda elt=elt: ViewRecipe(elt['name']))
            btn.place(x=27, y=240)
            timer = customtkinter.CTkImage(Image.open("timer.png"), size=(14, 14))
            customtkinter.CTkLabel(master=card, text="", image=timer).place(x=16, y=200)
            chef = customtkinter.CTkImage(Image.open("chefhat.png"), size=(15, 15))
            customtkinter.CTkLabel(master=card, text="", image=chef).place(x=104, y=200)
            person = customtkinter.CTkImage(Image.open("person.png"), size=(16, 16))
            customtkinter.CTkLabel(master=card, text="", image=person).place(x=60, y=200)
            customtkinter.CTkLabel(master=card, text=elt['duration'], font=("Arial", 12),
                                   text_color="#B6B5B5").place(
                x=38, y=200)
            customtkinter.CTkLabel(master=card, text=elt['people'], font=("Arial", 12), text_color="#B6B5B5").place(
                x=82, y=200)
            customtkinter.CTkLabel(master=card, text=elt['level'], font=("Arial", 12), text_color="#B6B5B5").place(
                x=126, y=200)

        def Filter():
            filters = {}
            combo1 = bycuisine.get()
            combo2 = bytaste.get()
            combo3 = bylevel.get()

            if combo1 != "Cuisine Type":
                filters["cuisine_type"] = combo1
            if combo2 != "Taste":
                filters["taste"] = combo2
            if combo3 != "Level":
                filters["level"] = combo3

            recipes = db.Recipes.find(filters, {"_id": 0, "name": 1, 'duration': 1, 'people': 1, "image": 1, "level": 1,
                                                "rating": 1})

            # filteredRecipes=list(recipes)


            n = 40
            m = 30
            num = 0

            bigframe = customtkinter.CTkFrame(master=mainframe, fg_color="#fdfbd8", width=1300, height=700)
            bigframe.place(x=200, y=70)
            # if len(filteredRecipes)==0:
            #     customtkinter.CTkLabel(master=bigframe, text="There is no corresponding recipe, Try another filter", fg_color="#fdfbd8", text_color="black", font=("Arial",26)).place(x=230, y=250)
            # def Saved():
            #     print("yahoooo")
            for elt in recipes:
                card = customtkinter.CTkFrame(master=bigframe, fg_color="white", width=235, height=290)
                card.place(x=n, y=m)
                n = n + 255
                num = num + 1
                if (num == 4):
                    m = m + 300
                    n = 40
                    num = 0

                photo = customtkinter.CTkImage(Image.open(elt['image']), size=(240, 140))
                customtkinter.CTkLabel(master=card, text="", image=photo).place(x=0, y=0)
                customtkinter.CTkLabel(master=card, text=elt['rating'], font=("Arial", 12), text_color="#6D1E16").place(
                    x=15, y=150)
                btnSave = customtkinter.CTkButton(master=card, text="save", corner_radius=32, fg_color="#6D1E16",
                                                  hover_color="#5B1613", width=40,
                                                  font=("Arial", 13), text_color='white',
                                                  command=lambda elt=elt: Saved(elt['name'],nameUs)
                                                  )
                btnSave.place(x=160, y=150)
                customtkinter.CTkLabel(master=card, text=elt['name'], font=("Arial", 16, "bold"),
                                       text_color="black").place(
                    x=15, y=175)
                btn = customtkinter.CTkButton(master=card, text="view recipe", corner_radius=32, fg_color="#6D1E16",
                                              hover_color="#5B1613",
                                              font=("Arial", 13), text_color='white', width=180,
                                              command=lambda elt=elt: ViewRecipe(elt['name']))
                btn.place(x=27, y=240)
                timer = customtkinter.CTkImage(Image.open("timer.png"), size=(14, 14))
                customtkinter.CTkLabel(master=card, text="", image=timer).place(x=16, y=200)
                chef = customtkinter.CTkImage(Image.open("chefhat.png"), size=(15, 15))
                customtkinter.CTkLabel(master=card, text="", image=chef).place(x=104, y=200)
                person = customtkinter.CTkImage(Image.open("person.png"), size=(16, 16))
                customtkinter.CTkLabel(master=card, text="", image=person).place(x=60, y=200)
                customtkinter.CTkLabel(master=card, text=elt['duration'], font=("Arial", 12),
                                       text_color="#B6B5B5").place(
                    x=38, y=200)
                customtkinter.CTkLabel(master=card, text=elt['people'], font=("Arial", 12), text_color="#B6B5B5").place(
                    x=82, y=200)
                customtkinter.CTkLabel(master=card, text=elt['level'], font=("Arial", 12), text_color="#B6B5B5").place(
                    x=126, y=200)

        btnFilter = customtkinter.CTkButton(master=mainframe, text="Filter", corner_radius=32, fg_color="#6D1E16",
                                      hover_color="#5B1613",
                                      font=("Arial", 13), text_color='white', width=120,height=30,
                                            command=Filter)

        btnFilter.place(x=610, y=40)










    mainframe = customtkinter.CTkFrame(app,fg_color="#fdfbd8")
    mainframe.pack(fill="both", expand=True)

    sidebar_frame = customtkinter.CTkFrame(master=mainframe, fg_color="white",  width=176, height=650, corner_radius=20)
    sidebar_frame.pack_propagate(0)
    sidebar_frame.pack(fill="y", anchor="w", side="left")


    logo_img =customtkinter.CTkImage(Image.open("logo.png"),size=(77.68, 85.42))
    customtkinter.CTkLabel(master=sidebar_frame, text="", image=logo_img).pack(pady=(38, 0), anchor="center")
    myfont = customtkinter.CTkFont(family="Arial", size=16, weight="bold")
    icon_dash =customtkinter.CTkImage(Image.open("dashboard.png"),size=(15,15))
    customtkinter.CTkButton(master=sidebar_frame, image=icon_dash, text="Dashboard", fg_color="transparent",text_color="black", font=myfont, hover_color="#fffdd1",command=lambda: Home(usernm), anchor="w").pack(anchor="center", ipady=5, padx=25, pady=(40, 0))
    icon_rec =customtkinter.CTkImage(Image.open("recipe.png"),size=(16,16))
    customtkinter.CTkButton(master=sidebar_frame, image=icon_rec, text="All Recipes", fg_color="transparent",text_color="black", font=myfont, hover_color="#fffdd1",command=AllRecipes, anchor="w").pack(anchor="center", ipady=5, padx=25, pady=(15, 0))
    icon_fv =customtkinter.CTkImage(Image.open("favorite.png"),size=(18,18))
    customtkinter.CTkButton(master=sidebar_frame, image=icon_fv, text="Saved", fg_color="transparent",text_color="black", font=myfont, hover_color="#fffdd1",command=lambda: SavedRecipes(nameUs), anchor="w").pack(anchor="center", ipady=5, padx=25, pady=(15, 0))
    icon_st =customtkinter.CTkImage(Image.open("settings.png"),size=(18,18))
    customtkinter.CTkButton(master=sidebar_frame, image=icon_st, text="Settings", fg_color="transparent",text_color="black", font=myfont, hover_color="#fffdd1", anchor="w").pack(anchor="center", ipady=5, padx=25, pady=(300, 0))

    expr="Welcome"+" "+usernm+" !"
    customtkinter.CTkLabel(master=mainframe, text=expr, text_color="black",font=("Arial",26,"bold")).pack(pady=(38, 0), padx=60 , anchor="w")

    def open_popup():
        recp = searchbar.get()

        if recp == "" :
            messagebox.showerror("Empty Field", "Search bar is empty")
        else:
            data = db.Recipes.find_one({"name": recp}, {"_id": 0})
            if data is None:
                messagebox.showerror("Not exists", "Recipe name doesn't exists")
            else:

                popup = customtkinter.CTk()
                popup.geometry("500x500")
                titre=data['name']
                popup.title(titre)
                popup.resizable(False, False)
                # photo=data.get("image","")
                # rec_img = customtkinter.CTkImage(Image.open("couscous.jpg"), size=(77.68, 85.42))
                # customtkinter.CTkLabel(master=popup, text="", image=rec_img).pack(pady=(38, 0),anchor="w")
                # print(photo)

                frame1 = customtkinter.CTkFrame(master=popup, fg_color="white", width=260, height=250,
                                                border_color="grey", border_width=1)
                frame1.place(x=0, y=0)
                customtkinter.CTkLabel(master=popup, text="Ingredients :", fg_color="white",text_color="#6D1E16", font=("Arial",18,"bold")).place(x=20, y=15)

                infos=data['ingredients']
                m=20
                for elt in infos:
                    customtkinter.CTkLabel(master=frame1, text=f"{elt}\n", font=("Arial", 14)).place(x=30, y=m)
                    m += 30

                frame2 = customtkinter.CTkFrame(master=popup, fg_color="white", width=240, height=250,
                                                border_color="grey", border_width=1)
                frame2.place(x=260, y=0)
                frame3 = customtkinter.CTkFrame(master=popup, fg_color="white", width=500, height=250,
                                                border_color="grey", border_width=1)
                frame3.place(x=0, y=250)
                customtkinter.CTkLabel(master=frame3, text="Method :", fg_color="white", text_color="#6D1E16",
                                       font=("Arial", 18, "bold")).place(x=20, y=15)
                text=data['method']
                textbox = customtkinter.CTkTextbox(frame3, width=300, fg_color="white", font=("Arial", 14))
                textbox.insert("0.0", text)
                textbox.configure(state="disabled")
                textbox.place(x=30, y=50)


                popup.mainloop()




    searchbar =customtkinter.CTkEntry(master=mainframe, placeholder_text="search by recipe name", corner_radius=32, fg_color="transparent",
                    border_color="grey",bg_color="#fdfbd8",
                    border_width=1,width=260, height=30)
    searchbar.place(x=965,y=38)

    search =customtkinter.CTkImage(Image.open("search.png"),size=(15,15))
    searchbtn=customtkinter.CTkButton(master=searchbar, image=search, text="", fg_color="transparent",
                            text_color="black", font=myfont, hover_color="#fffdd1",width=50,height=20, command=open_popup)
    searchbtn.place(x=205,y=3)


    banner=customtkinter.CTkFrame(master=mainframe, fg_color="white",  width=1000, height=200, corner_radius=20)
    banner.place(x=230,y=100)

    bannerimg = customtkinter.CTkImage(Image.open("thecook.jpg"), size=(300,230))
    customtkinter.CTkLabel(master=banner, text="", image=bannerimg).place(x=650,y=0)

    customtkinter.CTkLabel(master=banner, text="What Are You Craving ?", text_color="#6D1E16", font=('Arial',34,'bold')
                           ).place(x=85, y=50)
    customtkinter.CTkLabel(master=banner, text="Find Your Recipe Now !",
                           font=('Arial',18)
                           ).place(x=90, y=90)

    customtkinter.CTkButton(master=banner, text="Let's Go", corner_radius=32, fg_color="#6D1E16",
                            hover_color="#5B1613", width=60,
                            font=("Arial", 13), text_color='white', command=AllRecipes).place(x=380, y=120)

    customtkinter.CTkLabel(master=mainframe, text="Most Rated Recipes", text_color="black", font=("Arial", 20, "bold")).pack(
        pady=(265, 0), padx=60, anchor="w")

    def ViewRecipe(nom):
        data = db.Recipes.find_one({"name": nom}, {"_id": 0})
        popup = customtkinter.CTk()
        popup.geometry("500x500")
        titre = data['name']
        popup.title(titre)
        popup.resizable(False, False)


        frame1 = customtkinter.CTkFrame(master=popup, fg_color="white", width=260, height=250,
                                        border_color="grey", border_width=1)
        frame1.place(x=0, y=0)
        customtkinter.CTkLabel(master=popup, text="Ingredients :", fg_color="white", text_color="#6D1E16",
                               font=("Arial", 18, "bold")).place(x=20, y=15)

        infos = data['ingredients']
        m = 20
        for elt in infos:
            customtkinter.CTkLabel(master=frame1, text=f"{elt}\n", font=("Arial", 14)).place(x=30, y=m)
            m += 30

        frame2 = customtkinter.CTkFrame(master=popup, fg_color="white", width=240, height=250,
                                        border_color="grey", border_width=1)
        frame2.place(x=260, y=0)
        frame3 = customtkinter.CTkFrame(master=popup, fg_color="white", width=500, height=250,
                                        border_color="grey", border_width=1)
        frame3.place(x=0, y=250)
        customtkinter.CTkLabel(master=frame3, text="Method :", fg_color="white", text_color="#6D1E16",
                               font=("Arial", 18, "bold")).place(x=20, y=15)
        text = data['method']
        textbox = customtkinter.CTkTextbox(frame3, width=300, fg_color="white", font=("Arial", 14))
        textbox.insert("0.0", text)
        textbox.configure(state="disabled")
        textbox.place(x=30, y=50)

        popup.mainloop()

    def Saved(nom, usernm):
        donne = db.User.find_one({"username": usernm}, {"saved_recipes": 1, "_id": 0})
        exp = donne.get("saved_recipes", [])
        if nom not in exp:
            exp.append(nom)
        db.User.update_one({"username": usernm}, {"$set": {"saved_recipes": exp}})

    Mostrated=db.Recipes.find({"rating":{"$gte":8.0}},{"_id":0,"name":1,'duration':1,'people':1,"image":1,"level":1,"rating":1}).limit(4)
    n=230
    for elt in Mostrated:
        card = customtkinter.CTkFrame(master=mainframe, fg_color="white", width=235, height=290)
        card.place(x=n, y=380)
        n=n+255
        photo = customtkinter.CTkImage(Image.open(elt['image']), size=(240,140))
        customtkinter.CTkLabel(master=card, text="", image=photo).place(x=0,y=0)
        customtkinter.CTkLabel(master=card, text=elt['rating'], font=("Arial",12), text_color="#6D1E16").place(x=15, y=150)
        btnSave = customtkinter.CTkButton(master=card, text="save", corner_radius=32, fg_color="#6D1E16",
                                          hover_color="#5B1613", width=40,
                                          font=("Arial", 13), text_color='white',command=lambda elt=elt: Saved(elt['name'],nameUs)
                                  )
        btnSave.place(x=170, y=150)
        customtkinter.CTkLabel(master=card, text=elt['name'], font=("Arial", 16,"bold"), text_color="black").place(x=15,y=175)
        btn =customtkinter.CTkButton(master=card, text="view recipe", corner_radius=32, fg_color="#6D1E16", hover_color="#5B1613",
                    font=("Arial", 13), text_color='white', width=180, command=lambda elt=elt: ViewRecipe(elt['name']))
        btn.place(x=27,y=240)
        timer = customtkinter.CTkImage(Image.open("timer.png"), size=(14, 14))
        customtkinter.CTkLabel(master=card, text="", image=timer).place(x=16, y=200)
        chef = customtkinter.CTkImage(Image.open("chefhat.png"), size=(15, 15))
        customtkinter.CTkLabel(master=card, text="", image=chef).place(x=104, y=200)
        person = customtkinter.CTkImage(Image.open("person.png"), size=(16, 16))
        customtkinter.CTkLabel(master=card, text="", image=person).place(x=60, y=200)
        customtkinter.CTkLabel(master=card, text=elt['duration'], font=("Arial", 12), text_color="#B6B5B5").place(x=38,y=200)
        customtkinter.CTkLabel(master=card, text=elt['people'], font=("Arial", 12),text_color="#B6B5B5").place(x=82,y=200)
        customtkinter.CTkLabel(master=card, text=elt['level'], font=("Arial", 12),text_color="#B6B5B5").place(x=126,y=200)


def show_login_form():
    for widget in app.winfo_children():
        widget.destroy()

    def Login():
        mail=entry1.get()
        motpass=entry2.get()
        donnes=db.User.find_one({'email':mail,'password':motpass})
        if mail == "" or motpass == "":
            messagebox.showerror("Empty Field", "Kindly fill all the fields")
        else:
            donnes = db.User.find_one({'email': mail, 'password': motpass})
            if donnes is None:
                messagebox.showerror("Login Failed", "Incorrect email or password.")
            else:
                nomUt = db.User.find_one({'email': mail, 'password': motpass},{'username':1,"_id":0})
                username = nomUt.get('username', '')
                Home(username)


    my_image = customtkinter.CTkImage(Image.open("background.png"), size=(1300, 700))
    l1 = customtkinter.CTkLabel(app, image=my_image, text="")
    l1.pack(fill="both", expand=True)


    l2 = customtkinter.CTkLabel(master=l1, text="Log into your Account", font=('Arial', 24), bg_color="white")
    l2.place(x=540, y=240)

    entry1 = customtkinter.CTkEntry(master=l1, width=300, height=40, placeholder_text='Email', corner_radius=15, bg_color="white", fg_color="white")
    entry1.place(x=510, y=295)

    entry2 = customtkinter.CTkEntry(master=l1, width=300, height=40, placeholder_text='Password', show="*", corner_radius=15, bg_color="white", fg_color="white")
    entry2.place(x=510, y=345)

    btnfont = customtkinter.CTkFont(family="Arial", size=14, weight="bold")

    button1 = customtkinter.CTkButton(master=l1, width=130, height=40, text="Login", hover_color="#5B1613", text_color="white", corner_radius=15, bg_color="white", font=btnfont, fg_color="#6D1E16",
                                      command=Login)
    button1.place(x=510, y=400)

    l3 = customtkinter.CTkLabel(master=l1, text="Create your account", font=('Arial', 14), bg_color="white")
    l3.place(x=679, y=405)
    l3.bind("<Button-1>", lambda e: show_account_form())

def show_account_form():
    for widget in app.winfo_children():
        widget.destroy()

    def Inserer():
        nickname = entry5.get()
        mail = entry3.get()
        motpass = entry4.get()
        selected_country = combobox1.get()
        selected_gender = gender_var.get()


        if nickname == "" or mail == "" or motpass == "" or selected_country == "" or selected_gender == "":
            messagebox.showerror("Empty Fields", "Kindly fill all the fields")
        else:
            donnes = db.User.find_one({'email': mail})
            usrname = db.User.find_one({"username": nickname})

            if donnes is not None:
                messagebox.showerror("Exists", "Email already exists")
            elif usrname is not None:
                messagebox.showerror("Exists", "Username already exists")
            else:
                db.User.insert_one({
                    "username": nickname,
                    "email": mail,
                    "password": motpass,
                    "gender": selected_gender,
                    "country": selected_country
                })
                messagebox.showinfo("Account creation","Kindly log to your account")
                entry5.delete(0, 'end')
                entry3.delete(0, 'end')
                entry4.delete(0, 'end')
                combobox1.set('')
                gender_var.set('')


    my_image = customtkinter.CTkImage(Image.open("background2.png"), size=(1300, 700))
    l4 = customtkinter.CTkLabel(app, image=my_image, text="")
    l4.pack(fill="both", expand=True)

    l5 = customtkinter.CTkLabel(master=l4, text="Create your Account", font=('Arial', 24), bg_color="white")
    l5.place(x=540, y=220)
    entry3 = customtkinter.CTkEntry(master=l4, width=280, height=40, placeholder_text='Email', corner_radius=15,
                                    bg_color="white", fg_color="white")
    entry3.place(x=360, y=280)
    entry4 = customtkinter.CTkEntry(master=l4, width=280, height=40, placeholder_text='Password', corner_radius=15,
                                    bg_color="white", fg_color="white")
    entry4.place(x=660, y=280)
    entry5 = customtkinter.CTkEntry(master=l4, width=280, height=40, placeholder_text='Username', corner_radius=15,
                                    bg_color="white", fg_color="white")
    entry5.place(x=360, y=340)

    countries = [
        "Morocco",
        "United States",
        "Canada",
        "France",
        "Germany",
        "United Kingdom",
        "Australia",
        "Japan",
        "Brazil",
        "India",
        "South Africa"
    ]

    combobox1=customtkinter.CTkComboBox(master=l4, values=countries, width=280, height=40,corner_radius=15,
                                    bg_color="white", fg_color="white")
    combobox1.place(x=660, y=340)

    l7 = customtkinter.CTkLabel(master=l4, text="Gender :", font=('Arial', 16), bg_color="white")
    l7.place(x=362, y=400)
    gender_var = StringVar()
    radio_femme = customtkinter.CTkRadioButton(master=l4, text="Femme", variable=gender_var, value="Femme", fg_color="#6D1E16",bg_color="white")
    radio_femme.place(x=450, y=405)

    radio_homme = customtkinter.CTkRadioButton(master=l4, text="Homme", variable=gender_var, value="Homme", fg_color="#6D1E16",bg_color="white")
    radio_homme.place(x=540, y=405)

    btnfont = customtkinter.CTkFont(family="Arial", size=14, weight="bold")
    button2 = customtkinter.CTkButton(master=l4, width=130, height=40, text="Create", hover_color="#5B1613",
                                      text_color="white", corner_radius=15, bg_color="white", font=btnfont,
                                      fg_color="#6D1E16", command=Inserer)
    button2.place(x=362, y=445)

    l6 = customtkinter.CTkLabel(master=l4, text="You already have an account", font=('Arial', 14), bg_color="white")
    l6.place(x=752, y=450)
    l6.bind("<Button-1>", lambda e: show_login_form())


show_login_form()


app.mainloop()
