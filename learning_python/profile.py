# Define function with parameters
def profile_info(username, followers=1):
    print("Username: " + username)
    print("Followers: " + str(followers))

# Call function with parameters assigned as above
profile_info("sammyshark",)

# Call function with keyword arguments
profile_info(username="AlexAnglerfish", followers=342)
