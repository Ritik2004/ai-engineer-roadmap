document = """Ritik Tech Pvt Ltd - HR Policy. Employees get 24 paid leaves per year. \
Unused leaves can be carried forward up to 10 days. Sick leave is separate and allows \
12 days per year with a doctor's note. Work from home is allowed on Mondays and Fridays. \
Employees must be online between 10 AM and 4 PM on WFH days. The office is closed on \
the last Friday of every month. Laptop reimbursement limit is Rs 80,000, claimable once \
every 3 years. Internet bills up to Rs 1,000 per month are reimbursed for remote work. \
Health insurance covers employees and their parents up to Rs 5 lakh per year."""


def chunk_text(text,chunk_size,overlap):
    chunks=[]
    start=0
    while start<len(text):
        end = start+chunk_size
        chunks.append(text[start:end])
        start=end-overlap
    return chunks

chunks = chunk_text(document,chunk_size=150,overlap=50)

for i ,chunk in enumerate(chunks):
    print(f"---chunk {i} ({len(chunk)} chars)")
    print(chunk)