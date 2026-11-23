# Who Can Pay for the Transition

## Question
Canada's energy transition is happening in power and in capital spending,
not in what the country produces. The companies that must fund it earn
their cash from the fuels the transition is meant to replace. Which of
the 12 largest TSX-listed resource companies can pay for it?

## Answer in one paragraph
Five companies can pay comfortably: Barrick, Imperial, Agnico, Suncor
and Tourmaline combine a solid sustainability score with leverage under
one times EBITDA and coverage above 11 times. Three more can pay: CNQ,
Cenovus and Cameco have sound balance sheets and lower scores, and the
two energy names at the bottom of the scorecard score low because Bill
C-59 stripped their 2024 reports, not because they are weak. Two score
well but cannot pay comfortably: Nutrien and Methanex both scored 15
out of 20 and are the two most leveraged names in the set, at 3.04 and
4.05 times EBITDA. Teck is joint top of the scorecard and holds $7,587
million of cash from the coal sale, but its 2024 free cash flow was only
$155 million, so its ability to fund transition investment depends on
copper earnings. West Fraser is net cash, so its low Springate score is
a cyclical earnings trough, not distress.

## Files
- Who_Can_Pay_for_the_Transition_Report.pdf: combined report, formal,
  with the scorecard, the transition note, the credit models, the joint
  conclusion, and an appendix cataloguing every file.
- Who_Can_Pay_for_the_Transition_Model.xlsx: scorecard, credit models,
  2024 financials, transition summary, method.
- Who_Can_Pay_for_the_Transition_Notebook.ipynb: recomputation notebook.
- Canada-Energy-Transition-Note.md: standalone Part A note.
- Joint-Conclusion-Who-Can-Pay.md: standalone joint conclusion.
- credit/: Part B scripts, data, charts, and results note.
- data/: scorecard as data, the analysis CSVs, and the StatCan table
  metadata. The three full StatCan tables are 63 MB and are not in the
  repo; pull_statcan.py re-downloads them.
- charts/: Part A charts. credit/charts/: Part B charts.
- scripts/: Excel, notebook, and report builders for this combined
  package. The scorecard's own files are in energy-projects/.

## Method and limits
Scorecard: 4 measures scored 0 to 5 from each company's 2024
sustainability report, except Imperial Oil (2022, latest available).
Credit models: 2024 annual financials from Yahoo Finance, USD reporters
converted at USD/CAD 1.435. Merton is point-in-time at 31 December 2024.
Transition data: Statistics Canada tables 25-10-0015-01, 25-10-0029-01
and 34-10-0035-01. Ability to pay is not willingness to spend. Past
performance does not predict future performance. This project is an
investigation, not a credit rating and not personal investment advice.
