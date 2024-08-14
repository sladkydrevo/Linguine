# LINGUINE

The **Linguine web application** is a humble but sophisticated tool for every **linguist** or common user who wants to analyze and explore texts, or a language for that matter. It allows user to get information about text along with fancy tables and graphs, or search through text.

### Video Demo
https://www.youtube.com/watch?v=67j7qZITH2g

### The app – main page
On the main page, user first chooses from two functions - **analyze or explore**, while analyze being the default. User then inserts a text, either by **.txt file insertion or pasting to text area**. If using analysis, it is needed to choose a language – English or Czech, so the app works correctly since it uses **spaCy** library for the text processing. 

## Analyze 
Perhaps the most important utility of Linguine: the analyze function. It processes text using the powerful **spaCy** library. The application supports both **English and Czech**, and the spaCy library enables the extraction of linguistic features such as tokenization, lemmatization, and part-of-speech tagging, which are essential for any text analysis.

The function generates various statistical insights:
- **Character, Token, Type and Sentence Counts**: Provides fundamental metrics on the text structure.
- **Type-Token Ratio (TTR)**: A measure of lexical diversity, indicating the richness of the vocabulary used.
- **Average Word and Sentence Lengths**: These metrics can indicate the complexity of the text.

Next to these, there is a table showing more detailed insights, such as
- **The Most Frequent Noun, Adjective and Verb**: Displays the most commonly used words along with their frequencies.
- **The Longest Words**: Lists the longest words in the text, including multiple words of the same length if applicable.

### Tokens spaCy table
On the right side, user gets a **table** containing all the tokens of the text along with their **lemma form, part-of-speech, syntactic dependency, and stopword status**. The table is **scrollable** and has a **filter** for searching specific words. Users can **sort** the table by clicking on the header items, and it also supports exporting the data in CSV format.


### Graphs
Below these features, three interactive graphs—**histograms and a scatter plot**—created with the Plotly library provide visual representations of the data:
- **Sentence Length Distribution**: A histogram displaying the distribution of sentence lengths.
- **Word Length Distribution**: A histogram showing the distribution of word lengths.
- **Sentence Length Progression**: A scatter plot tracking the progression of sentence lengths throughout the text.

These graphs are fully interactive and can be downloaded for further analysis.

## Explore 
The Explore function utilizes **regular expressions** to allow users to search for specific patterns or phrases within the text. 
The expression is highlighted in each returned **sentence** and each sentence also shows the **number of words** in the sentence and is classified as **declarative, interrogative, or exclamatory**.

## Profile
User can **register** into the app with username and password. Registered users can **save texts**, making it easier to revisit and analyze them later. The application securely stores user data in a **MySQL database**, ensuring that texts are easily accessible while maintaining data integrity. User can find the saved texts in the My texts tab, which works the same way as the main page with user choosing from the saved texts. User can also delete texts by clicking on a delete button. 

User passwords are securely **hashed** using Werkzeug's password hashing tools, ensuring that even if the database is compromised, user credentials remain protected. The use of session management also ensures that user data is handled securely across different sessions.

## Linguistic terms
List of **linguistic terms** used in the web app, especially in the analysis part.

### About the Developer
Tereza is a double major student at the Palacký University in Olomouc, Czechia, who's fields of study are General Linguistics, Theory of Communication and Digital Humanities. She was born in Prague, Czechia, has a cat, has a love-hate relationship with coding, and in the free time surfs the 한류 big style. 

And this was CS50! <3