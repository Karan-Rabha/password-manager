def save_file(userdata, save_to_path):
    print(save_to_path)
    website=userdata["website"]
    email= userdata["email"]
    password= userdata["password"]
    with open(f"{save_to_path}/password manager.txt", mode="a+") as f:
        f.write(f"website -- {website}, email -- {email}, password -- {password}\n")
    return True


def get_data(save_to_path):
    user_data= {}
    try:
        with open(f"{save_to_path}/password manager.txt", mode="r") as f:
            data = f.readlines()
            for line in data:
                ## data cleaning
                split_data= line.split(",")
                website= split_data[0].split("--")[1].strip()
                email= split_data[1].split("--")[1].strip()
                password= split_data[2].split("--")[1].strip()
                ## adding cleaned data in the empty dictionary
                user_data[website]= {"email":email,"password":password}
    except FileNotFoundError:        
        pass
    finally:
        return user_data
