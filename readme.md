This program uses a public dictionary I found online.  The five_letter_words.json file is a result of me parsing out only words with 5 letters from that dictionary.

The Python script takes the input from the dictionary, runs it through Wordle (using Selenium to control the browser) and appends valid words to the "valid_words.csv" file.

Because there are so many five letter words I added the ability to only check words which begin with a certain letter.  This lets me deal with smaller "chunks" of letters and then append them to the CSV.  This is necessary because I have calculated the time each word takes to be processed to be ~2.2 seconds.  With about 16,000 words in the dictionary it would take ~9 hours 48 minutes to run through the entire file.

So far I have only run through the words starting with "A" but I will update this repo eventually for each letter.

To run this script you will need to have Chrome 98 and the driver for it (downloadable the latest stable release here: https://sites.google.com/chromium.org/driver/).  The downloaded file will need to be placed in your Operating Systems PATH (For Ubuntu just put the file in /usr/bin or /usr/local/bin, for Windows it is a bit more involved but instructions are available online)