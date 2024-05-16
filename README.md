# Spectrum-Webmail-Clearer

## Efficiently clears emails on Spectrum Webmail

Spectrum Webmail has a very slow interface that makes clearing emails a time-intensive process. My grandma ran out of storage, so I wrote this Python script to automate the mass deletion of her old emails. It's by no means clean or optimized, but it gets the job done. 

## Usage

1. Clone the repository onto your local machine, or just copy the lone Python file.
2. Install dependencies.
3. Run the script, following the prompts.

### Notes

* Here I assume an emails-per-page setting of 100, but if the user prefers a lower number they can reduce the final wait time, although this does reduce efficiency.
* Currently, it will delete 100 emails every 2.5 minutes, starting at the oldest set of emails.
* The current implementation has been tailored to Google Chrome.
