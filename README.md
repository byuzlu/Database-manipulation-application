Welcome to the Online Auction System! This project aims to design a comprehensive data management system similar to eBay, tailored to handle user accounts, auctions, payments, and billing seamlessly. Here's an overview of the system's key features and functionalities:

User Management
Every user has essential details including first name, last name, password, date of birth, and social security number. Users can be categorized as admins, buyers, or sellers. Sellers have an associated IBAN, while buyers are linked to at least one payment information record.

Auction Management
Auctions are initiated by sellers and must be accepted by an admin before becoming active. Each auction has a starting and ending date, title, description, status, starting price, current price, and a "buy it now" option. Auctions are categorized, and each auction can have multiple bids by buyers. The auction concludes either when a buyer uses the "buy it now" option or when the auction reaches its ending date.

Bidding Process
Buyers can place multiple bids on an auction, with the current price dynamically updated based on the maximum bidder's offer. The highest bidder wins the auction and selects one of their payment information records for payment.

Payment and Billing
Once the auction concludes, a bill is generated, including a unique transaction number and net amount. The company receives an 8% commission from the selling price. Each bill is associated with a seller, who can have multiple bills.

System Operation
To simplify the project, a manual "end the auction" button is provided to conclude auctions. This triggers the billing process and ensures smooth operation.

Next Steps
Future enhancements could include implementing automatic auction closure based on ending dates, refining the bidding process, and enhancing the user interface for a seamless user experience.

Contribution and Support
Contributions and feedback are welcome to enhance the functionality and usability of the Online Auction System. For any questions or assistance, please contact baha.yuzlu@gmail.com. Thank you for your interest and support as we continue to develop and improve the system.

