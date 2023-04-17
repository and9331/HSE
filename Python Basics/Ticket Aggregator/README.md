## Ticket Aggregator

Flight booking sites or 'airfare aggregators' have become one of the most useful sources to aggregate amounts of information about destinations, flights, airlines, and airfares. You have either heard or used at least one of the flight search sites like Travelocity, Expedia, CheapOair, TripAdvisor Flights, or Skyscanner. Before the pandemic, people used to spend a lot of time on these sites.

Image's source: www.thehoneymoondestinations.com

However, not all people find these sites helpful and come up with their ticket aggregators. Once, I was scrolling towardsdatascience.com when I found this article, and it inspired me to give you the following assignment.

#### Assignment Instructions

Imagine you need to develop your airfare aggregator. Let's assume that your aggregator will be posted on a website that is used for searching Moscow - New York flights. Your solution should be based on the following results of the customer research. There are some quotes from the brief:

- There are four criteria that people value the most: the ticket price, the number of transfers, a refund (either included or not), and luggage (either included or not);

- The cheaper, the better! People say that the best offer is the one which costs less than $200; it should be either a direct flight or a flight with one transfer; refund is included; luggage is included;

- Then, customers say that they consider an offer 'good enough' if its price is in a range from $200 to $250; it is either a direct flight or might require one or two transfers; refund is either included or not; the same for luggage - it is either included or not;

- Finally, customers claim that the worst offer is the one which price is more than $250; three and more transfers are required; refund is either included or not; the same for luggage - it is either included or not.

### Step-by-step Instructions

Now, what we expect you to do!

Write a program that gets as input the data on these criteria. The data is entered from the keyboard. Think about the way you organize the input, transform the data, and check whether the data are entered in a right way. Then the program should classify an offer based on these criteria and print on the screen an offer category and this offer's description. You need to come up with the classification rule based on the information from the brief. In principle, the output should be one of the four categories, which are 'the best', 'good enough', 'bad', and 'other' (for those which cannot be classified as either of three main categories). Use Boolean conditions and if / if-else / if-elif-else constructions.

Analyze the aggregator based on the information from the brief. Describe its advantages and disadvantages. Do you personally find these criteria and this classification rule convincing? Use words, not a code.

Suggest your alternative solution. Propose other criteria, completely different way of categorizing offers, different categories themselves - whatever you think should enhance the aggregator based on the brief. You are supposed, first, describe it in words, and, second, show your code.

Complete the task in Jupyter Notebook. Insert the programming code in code cells and text explanations in markdown cells. Make sure that you name your file appropriately (e.g. SGA1_Ticket_Aggregator_[your surname].ipynb).