import pdfplumber
import re

def extract_cutoffs_from_pdf(pdf_path):
    data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            # print(text)

            # Regex pattern to extract college name, branch, and cut-offs
            college_pattern = re.compile(r'(\d{4}\s*-\s*[A-Za-z\s]+),')
            branch_pattern = re.compile(r'(\d{9}\s*-\s*[A-Za-z\s]+)')
            cutoff_pattern = re.compile(r'(\b[A-Z]+\b\s+I\s+\d+\s+\([\d.]+\))')

            # Find all instances of college names, branches, and cut-offs
            colleges = college_pattern.findall(text)
            branches = branch_pattern.findall(text)
            # cutoffs = cutoff_pattern.findall(text)

            if colleges and branches: # and cutoffs:
                for college, branch in zip(colleges, branches):
                    college_data = {
                        "college_name": college.strip(),
                        "branch_name": branch.strip(),
                        # "cutoffs": {}
                    }
                    # for cutoff in cutoffs:
                    #     category, rank = cutoff.split(' ')[0], cutoff.split(' ')[2]
                    #     college_data["cutoffs"][category] = rank
                    data.append(college_data)
            print(data)
    
    return data

# Call the function
pdf_path = "C:/Users/suraj/Projects/college-clarity/data/cet/2022ENGG_CAP1_CutOff.pdf"
cutoff_data = extract_cutoffs_from_pdf(pdf_path)

# Example: Print the first few entries
# for entry in cutoff_data[:5]:
#     print(entry)
