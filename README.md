
# Email that sends the official USD:MXN rate

## What it does

The script will get the official USD:MXN exchange rate:

- For the current month.
- For the year to date.
- The rate for the next 2-4 days

It will then create three separate graphs showing:

1. The exchange rate for the current month and the next 2-4 days.

2. The echange rate for the current year.

3. The exchange rate for the current year.

The first two graphs lower and upper limits are dictated by the minimum and maximum values of the exchange rate, and show in detail the changes in the exchange rate.

The last graph is the same as the second graph, but uses a limit of 0 in the Y axis, to view the changes in rate from an absolute perspective.

Graph of the exchange rate for the current month and the next 2-4 days:

![Current Month Exchange Rate](/TipoDeCambioMes.png)

Graph of exchange rate for the current year:

![Current Year Exchange Rate](/TipoDeCambioYtd.png)

Graph of exchange rate for the current year with Y axis minimum at 0:

![Current Year Exchange Rate Yaxis in 0](/TipoDeCambioYtdAbs.png)

After that it will calculate the Gain or Loss values for the month, both in absolute terms and as a percentage change. It will then compare against a threshold value.

If the change is higher than the threshold, it will recomend to buy or sell a security to avoid paying the FX gain or o create an FX loss.

If the change is lower than the threshold value, it will recommend to wait.

Finally, it will build an email body with the FX information for the month and the recommendation. It will then send the email to a recipient, along with the attached graphs.

You can find an example email [here.](/example_email.pdf)

## How it works

The file is separated in to three different scripts:

- send_email.py: Contains the Class used to send an email.
- get_fx.py: Contains the Class that creates the graphs and calculations.
- main_fx: Creates the objects and executes the code to create each graph, make the calculations and send the email.

Here is a diagram of how the scripts works:

![Script Diagram](/FX_Email_Diagram.png)

## How to Use

To execute the code you will need to install the following libraries:

- os
- pandas
- smtplib
- requests
- datetime
- matplotlib
- import imghdr

The libraries installed in my virtual enviroment and their versions are in the requirements.txt file.

To be able to send an email, you will also have to get an email token and its smtp address. If you use gmail, you can find a tutorial on how to do that [here.](https://realpython.com/python-send-email/)

You will also need to hard code  your username and password in the send_email.py script, or save it as an enviroment variable in your computer and access it with the os.environ.get() function. This second approach is much more secure and highly recommended.

To change the email recipient list or the attachment names, change the code in main_fix.py

To execute the script automatically, you can run a cron service or its equivalent and automate the execution of the script on a monthly basis.

## How to Use

I use the script to monitor the amount of cash in USD denominated accounts.

Any Mexican resident or Mexcan Company will calculate FX gains on a monthly basis, and will have to pay taxes accordingnly. By monitoring FX gains or losses, you can minimize the amount of cash succeptible to FX gains and thus have a more efficient cash managment process.
