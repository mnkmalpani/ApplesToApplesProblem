# A4A Problem Statement

Given 2 documents "Buyer.csv" & "Supplier.csv", build a solution that reconciles / matches the txns. The solution should -:

\1. categorize the txns into Exact / Partial / Only in Buyer / Only in Supplier categories

\2. handle matching of number / string / date

**Definitions**

Exact Match - 2 elements are an exact match if they are exactly the same

Partial Match - 

1. Number1, Number2 match partially if Number2 is in range of Number1 +/- threshold
1. String1, String2 match partially if String2 is similar to String1
1. Date1, Date2 match partially if Date2 is in range of Date1 +/- threshold
1. \*If there are multiple partial matches, the ‘best partial match’ should show up

**Notes**

1. Working code is super important
1. Code quality is table stakes
1. System Design should be Extensible / Flexible
1. Can use open source libraries with proper justification

**Example**

Doc1

Name    RegNum  Salary

Ram     12A3    9000

Shyam   12A4    8500

Sita	   12A6   7500

Doc2

Name    RegNum  Salary

Rama     12A3    9000

Shyam   12A4$    8501

GhanShyam 12A5 8500

Sita	   12A6   7500


Output

Name    RegNum  Salary  	Category    	Name    RegNum  Salary

Ram     12A3         9000    	Partial     	Rama     12A3    9000

Shyam  12A4       8500    	Partial     	Shyam   12A4$    8501

GhanShyam 12A5 8500 	Only

Sita	   12A6   7500.            Exact              Sita	   12A6   7500



