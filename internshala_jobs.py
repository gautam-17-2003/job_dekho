import requests
from bs4 import BeautifulSoup
import csv

def scrape_internshala_jobs(url, num_pages):
    # Open a CSV file for writing
    with open('internshala_jobs.csv', 'w', newline='', encoding='utf-8') as csv_file:
        # Create a CSV writer object
        csv_writer = csv.writer(csv_file)

        # Write header row to CSV
        csv_writer.writerow(['Job Title', 'Company', 'Location', 'CTC', 'Experience Required'])

        for page in range(1, num_pages + 1):
            page_url = f"{url}?page={page}"
            response = requests.get(page_url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                job_listings = soup.find_all("div", class_="individual_internship")

                for index, listing in enumerate(job_listings, start=1):
                    job_title_element = listing.find("h3", class_="heading_4_5")
                    job_title = job_title_element.text.strip() if job_title_element else "Job title not found"

                    company_element = listing.find("a", class_="link_display_like_text")
                    company = company_element.text.strip() if company_element else "Company name not found"

                    location_element = listing.find("a", class_="location_link")
                    location = location_element.text.strip() if location_element else "Location not found"

                    stipend_element = listing.find("div", class_="salary")
                    stipend = stipend_element.find_next("span").text.strip() if stipend_element else "Stipend not found"

                    exp_element = listing.find("div", class_="job-experience-item")
                    exp = exp_element.find_next("div").find_next("div").text.strip() if exp_element else "Exp not found"

                    # Write the job data to the CSV file
                    csv_writer.writerow([job_title, company, location, stipend, exp])
                    
                    # Print a message for each job
                    print(f"Job {index} details written to CSV file.")

            else:
                print(f"Error: Received status code {response.status_code}. Page {page} not loaded successfully.")

if __name__ == "__main__":
    internshala_url = "https://internshala.com/jobs"
    num_pages_to_scrape = 4
    scrape_internshala_jobs(internshala_url, num_pages_to_scrape)
    print("Job data has been successfully written to 'internshala_jobs.csv'.")
