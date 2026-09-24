class JobMarketplace:
    def __init__(self):
        self.job_listings = []
        self.resumes = []

    def post_job(self, title, company, requirements):
        job = {
            "title": title,
            "company": company,
            "requirements": requirements,
        }
        self.job_listings.append(job)

    def remove_job(self, title, company, requirements):
        job = {
            "title": title,
            "company": company,
            "requirements": requirements,
        }
        self.job_listings.remove(job)

    def submit_resume(self, name, skills, experience):
        resume = {
            "name": name,
            "skills": skills,
            "experience": experience,
        }
        self.resumes.append(resume)

    def withdraw_resume(self, name, skills, experience):
        resume = {
            "name": name,
            "skills": skills,
            "experience": experience,
        }
        self.resumes.remove(resume)

    def search_jobs(self, query):
        query_lower = query.lower()
        results = []
        for job in self.job_listings:
            if query_lower in job["title"].lower():
                results.append(job)
                continue
            for requirement in job["requirements"]:
                if query_lower in requirement.lower():
                    results.append(job)
                    break
        return results

    def get_job_applicants(self, job):
        applicants = []
        for resume in self.resumes:
            if self.matches_requirements(resume, job):
                applicants.append(resume)
        return applicants

    @staticmethod
    def matches_requirements(resume, job):
        for skill in resume["skills"]:
            if skill not in job["requirements"]:
                return False
        return True

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
