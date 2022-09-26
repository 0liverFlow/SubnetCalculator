def menu():
    user_choice = -1
    print('=========================================================================')
    while not(user_choice >=0 and user_choice < 4):
        user_choice = int(input("|\t\t\tEnter : \n\
|>1.Only calculate the net and the host id of the network.\n\
|>2.Divide the network into x given subnets(FLSM).\n\
|>3.Divide the network based on the number of users(VLMS).\n\
|>Thanks to elucidate your choice (you have to just enter 1, 2 or 3) : "))
    print('|========================================================================')
    return user_choice

