# Database Admin - Example Interactions

## List Employees

**User**: "Show me all employees"

**Agent Response**:

```
📋 EMPLOYEE LIST (15 total)
━━━━━━━━━━━━━━━━━━━━━━━━━━━

ID | Name               | Department   | Job Title
---|--------------------|--------------|--------------------------
1  | John Smith         | Engineering  | Senior Software Engineer
2  | Sarah Johnson      | Engineering  | Tech Lead
3  | Michael Williams   | Sales        | Sales Manager
4  | Emily Brown        | Marketing    | Marketing Director
5  | David Jones        | Engineering  | DevOps Engineer
6  | Jessica Garcia     | HR           | HR Manager
7  | James Miller       | Finance      | Financial Analyst
8  | Amanda Davis       | Engineering  | Frontend Developer
9  | Robert Martinez    | Sales        | Account Executive
10 | Lisa Anderson      | Marketing    | Content Strategist

Showing 10 of 15 employees. Use limit parameter for more.
```

## Get Employee by ID

**User**: "Tell me about employee #2"

**Agent Response**:

```
👤 EMPLOYEE DETAILS
━━━━━━━━━━━━━━━━━━━

📌 ID: 2
👤 Name: Sarah Johnson
📧 Email: sarah.johnson@company.com
🏢 Department: Engineering
💼 Title: Tech Lead
💰 Salary: $120,000
📅 Hire Date: 2018-06-20
📱 Phone: +1-555-0102
📍 City: San Francisco

Sarah is one of our senior Engineering team members,
leading technical initiatives since 2018.
```

## Search Employees

### By Department

**User**: "Find all engineers"

**Agent Response**:

```
🔍 SEARCH RESULTS: Engineering Department
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Found 5 employees:

ID | Name           | Job Title                | Salary
---|----------------|--------------------------|--------
1  | John Smith     | Senior Software Engineer | $95,000
2  | Sarah Johnson  | Tech Lead                | $120,000
5  | David Jones    | DevOps Engineer          | $90,000
8  | Amanda Davis   | Frontend Developer       | $85,000
11 | William Taylor | Backend Developer        | $88,000
15 | Daniel White   | QA Engineer              | $78,000

Engineering has the largest team with 5 members.
Average salary: $92,667
```

### By Name

**User**: "Find employee named John"

**Agent Response**:

```
🔍 SEARCH RESULTS: "John"
━━━━━━━━━━━━━━━━━━━━━━━━━

Found 1 employee:

👤 John Smith
   📧 john.smith@company.com
   🏢 Engineering | Senior Software Engineer
   💰 $95,000 | 📍 San Francisco
   📅 Hired: 2020-03-15
```

### By City

**User**: "Who works in San Francisco?"

**Agent Response**:

```
🔍 EMPLOYEES IN SAN FRANCISCO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Found 4 employees:

ID | Name           | Department   | Title
---|----------------|--------------|------------------------
1  | John Smith     | Engineering  | Senior Software Engineer
2  | Sarah Johnson  | Engineering  | Tech Lead
8  | Amanda Davis   | Engineering  | Frontend Developer
15 | Daniel White   | Engineering  | QA Engineer

San Francisco is our main Engineering hub!
```

## Department Statistics

**User**: "Show department stats"

**Agent Response**:

```
📊 DEPARTMENT STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━

Company Total: 15 employees
Company Avg Salary: $82,867

Department   | Employees | Avg Salary | Min      | Max
-------------|-----------|------------|----------|----------
Engineering  | 5         | $92,667    | $78,000  | $120,000
Sales        | 3         | $72,333    | $62,000  | $85,000
Marketing    | 2         | $91,000    | $72,000  | $110,000
Finance      | 2         | $74,000    | $68,000  | $80,000
HR           | 2         | $70,000    | $65,000  | $75,000

📈 Insights:
• Engineering is the largest department (33%)
• Marketing has highest avg salary among smaller depts
• Company-wide salary range: $62K - $120K
```

## Combined Queries

**User**: "Compare sales and engineering teams"

**Agent Response**:

```
⚖️ TEAM COMPARISON: Engineering vs Sales
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                   | Engineering | Sales
-------------------|-------------|--------
Team Size          | 5           | 3
Avg Salary         | $92,667     | $72,333
Salary Range       | $78K-$120K  | $62K-$85K
Top Earner         | Sarah J.    | Michael W.
                   | ($120K)     | ($85K)
Cities             | SF, Seattle | NY, LA

Engineering team is larger with higher compensation,
reflecting the tech-focused nature of the company.
```
