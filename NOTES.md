__QIF Format__
--------------
Format:
    // File header
    !Account     //header
    N<Account>   //account name
    T<Type>      //type
    ^            //end of header
    !Type:<Type> //account type
    // Transaction
    D<Date>      //date in MM/DD/YYYY
    T<Amount>    //dollar (negative if header account decrease)
    L<Account>   //other account (debit or credit)
    M<Memo>      //memo

Example:
    !Account
    NAssets:Current Assets:Cash
    TCash
    ^
    !Type:Cash
    D11/02/2012
    T-5.02
    LExpenses:Parking
    MPaid for parking.

