class JobMarketplace:
    def __init__(self):
        self.job_listings = []
        self.resumes = []

    def get_job_applicants(self, job: dict) -> list:
        applicants = []
        for resume in self.resumes:
            matches = self.matches_requirements(resume, job["requirements"])
            if matches:
                applicants.append(resume)
        return applicants

    def matches_requirements(self, resume: object, requirements: collection) -> boolean:
        for skill in resume["skills"]:
            missing_skill_check = skill not in requirements
            if missing_skill_check:
                return False
        return True

    def post_job(self, job_title: string, company: string, requirements: list):
        job = {
            "job_title": job_title,
            "company": company,
            "requirements": requirements,
        }
        self.job_listings.append(job)

    def remove_job(job: any):
        job_listings = self.job_listings
        job = job
        job_listings.remove(job)

    def search_jobs(self: object, criteria: string) -> list:
        matching_jobs = []
        criteria_lower = criteria.lower()
        for job_listing in self.job_listings:
            match_check = criteria_lower in job_listing["job_title"].lower() or any(
                criteria_lower == str(requirement).lower()
                for requirement in job_listing["requirements"]
            )
            if match_check:
                matching_jobs.append(job_listing)
        return matching_jobs

    def submit_resume(name: any, skills: any, experience: any):
        resume = {
            "name": name,
            "skills": skills,
            "experience": experience,
        }
        self.resumes.append(resume)

    def withdraw_resume(self: object, resume: any) -> null:
        resumes_collection = self.resumes
        resume_to_remove = resume
        resumes_collection.remove(resume_to_remove)

import unittest

class JobMarketplaceTestPostJob(unittest.TestCase):
    def test_post_job(self):
        jobMarketplace = JobMarketplace()
        jobMarketplace.post_job("Software Engineer", "ABC Company", ['requirement1', 'requirement2'])
        self.assertEqual(jobMarketplace.job_listings, [{'job_title': 'Software Engineer', 'company': 'ABC Company', 'requirements': ['requirement1', 'requirement2']}])

    def test_post_job_2(self):
        jobMarketplace = JobMarketplace()
        jobMarketplace.post_job("Mechanical Engineer", "XYZ Company", ['requirement3', 'requirement4'])
        self.assertEqual(jobMarketplace.job_listings, [{'job_title': 'Mechanical Engineer', 'company': 'XYZ Company', 'requirements': ['requirement3', 'requirement4']}])

    def test_post_job_3(self):
        jobMarketplace = JobMarketplace()
        jobMarketplace.post_job("Software Engineer", "ABC Company", ['requirement1', 'requirement2'])
        jobMarketplace.post_job("Mechanical Engineer", "XYZ Company", ['requirement3', 'requirement4'])
        self.assertEqual(jobMarketplace.job_listings, [{'job_title': 'Software Engineer', 'company': 'ABC Company', 'requirements': ['requirement1', 'requirement2']}, {'job_title': 'Mechanical Engineer', 'company': 'XYZ Company', 'requirements': ['requirement3', 'requirement4']}])

    def test_post_job_4(self):
        jobMarketplace = JobMarketplace()
        jobMarketplace.post_job("Software Engineer", "ABC Company", ['requirement1', 'requirement2'])
        jobMarketplace.post_job("Mechanical Engineer", "XYZ Company", ['requirement3', 'requirement4'])
        jobMarketplace.post_job("Software Engineer", "ABC Company", ['requirement1', 'requirement2'])
        self.assertEqual(jobMarketplace.job_listings, [{'job_title': 'Software Engineer', 'company': 'ABC Company', 'requirements': ['requirement1', 'requirement2']}, {'job_title': 'Mechanical Engineer', 'company': 'XYZ Company', 'requirements': ['requirement3', 'requirement4']}, {'job_title': 'Software Engineer', 'company': 'ABC Company', 'requirements': ['requirement1', 'requirement2']}])

    def test_post_job_5(self):
        jobMarketplace = JobMarketplace()
        jobMarketplace.post_job("Software Engineer", "ABC Company", ['requirement1', 'requirement2'])
        jobMarketplace.post_job("Mechanical Engineer", "XYZ Company", ['requirement3', 'requirement4'])
        jobMarketplace.post_job("Software Engineer", "ABC Company", ['requirement1', 'requirement2'])
        jobMarketplace.post_job("Mechanical Engineer", "XYZ Company", ['requirement3', 'requirement4'])
        self.assertEqual(jobMarketplace.job_listings, [{'job_title': 'Software Engineer', 'company': 'ABC Company', 'requirements': ['requirement1', 'requirement2']}, {'job_title': 'Mechanical Engineer', 'company': 'XYZ Company', 'requirements': ['requirement3', 'requirement4']}, {'job_title': 'Software Engineer', 'company': 'ABC Company', 'requirements': ['requirement1', 'requirement2']}, {'job_title': 'Mechanical Engineer', 'company': 'XYZ Company', 'requirements': ['requirement3', 'requirement4']}])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
