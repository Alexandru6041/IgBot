# IgBot
## ***RULES:***
1. DISABLE 2FA AUTHENTICATION
2. FOLLOW IN ADVANCE EVERY ACCOUNT THAT YOU WANT TO SEND THE MESSAGE TO
3. PASTE IN YOUR CLIPBOARD THE MESSAGE YOU WANT TO SEND
      - **otherwise ```EmptyClipboard_ERROR``` exception will be raised**
<br/><br/>
4. WRITE THE LIST OF ALL YOUR ACCOUNTS THAT YOU WANT TO SEND THE MESSAGES TO:

   - Manually introduce them into the ```AccountsTable``` in ```db.sqlite``` file
   - Go to ```app.py```, go to ***line 184*** and paste into the ```accounts``` list the accounts reffered above and also uncomment ***lines from 184 to 187*** included:
      - ```
         184.   accounts = []
         185.   for i in range(len(accounts)):
         186.     Db.InsertData("AccountsTable", accounts[i])
         187.   print("Data Inserted")
         ```
      - Formatting example: 
         - ```accounts = ['account1', 'account2', 'account3']```
<br/><br/>
5. RESTART THE CODE