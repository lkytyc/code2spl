class JobMarketplace:
    def __init__(self):
        self.job_listings = []
        self.resumes = []

    def post_job(self, job_title, company, requirements):
        job = {
            "job_title": job_title,
            "company": company,
            "requirements": requirements,
        }
        self.job_listings.append(job)

    def remove_job(self, job):
        self.job_listings.remove(job)

    def submit_resume(self, name, skills, experience):
        resume = {
            "name": name,
            "skills": skills,
            "experience": experience,
        }
        self.resumes.append(resume)

    def withdraw_resume(self, resume):
        self.resumes.remove(resume)

    def search_jobs(self, criteria):
        matching_jobs = []
        for job_listing in self.job_listings:
            if criteria.lower() in job_listing["job_title"].lower():
                matching_jobs.append(job_listing)
            else:
                requirements_lower = [r.lower() for r in job_listing["requirements"]]
                if criteria.lower() in requirements_lower:
                    matching_jobs.append(job_listing)
        return matching_jobs

    def get_job_applicants(self, job):
        applicants = []
        for resume in self.resumes:
            if self.matches_requirements(resume, job["requirements"]):
                applicants.append(resume)
        return applicants

    def matches_requirements(self, resume, requirements):
        for skill in resume["skills"]:
            if skill not in requirements:
                return False
        return True

import unittest

class JobMarketplaceTestSearchJobs(unittest.TestCase):
    def test_search_jobs(self):
        jobMarketplace = JobMarketplace()
        jobMarketplace.job_listings = [{"job_title": "Software Engineer", "company": "ABC Company", "requirements": ['skill1', 'skill2']}]
        self.assertEqual(jobMarketplace.search_jobs("skill1"), [{'job_title': 'Software Engineer', 'company': 'ABC Company', 'requirements': ['skill1', 'skill2']}])

    def test_search_jobs_2(self):
        jobMarketplace = JobMarketplace()
        jobMarketplace.job_listings = [{"job_title": "Software Engineer", "company": "ABC Company", "requirements": ['skill1', 'skill2']}, {"job_title": "Software Engineer", "company": "ABC Company", "requirements": ['skill3', 'skill4']}]
        self.assertEqual(jobMarketplace.search_jobs("skill1"), [{'job_title': 'Software Engineer', 'company': 'ABC Company', 'requirements': ['skill1', 'skill2']}])

    def test_search_jobs_3(self):
        jobMarketplace = JobMarketplace()
        jobMarketplace.job_listings = [{"job_title": "Software Engineer", "company": "ABC Company", "requirements": ['skill1', 'skill2']}, {"job_title": "Software Engineer", "company": "ABC Company", "requirements": ['skill3', 'skill4']}]
        self.assertEqual(jobMarketplace.search_jobs("skill3"), [{'job_title': 'Software Engineer', 'company': 'ABC Company', 'requirements': ['skill3', 'skill4']}])

    def test_search_jobs_4(self):
        jobMarketplace = JobMarketplace()
        jobMarketplace.job_listings = [{"job_title": "Software Engineer", "company": "ABC Company", "requirements": ['skill1', 'skill2']}, {"job_title": "Software Engineer", "company": "ABC Company", "requirements": ['skill3', 'skill4']}]
        self.assertEqual(jobMarketplace.search_jobs("skill5"), [])

    def test_search_jobs_5(self):
        jobMarketplace = JobMarketplace()
        jobMarketplace.job_listings = [{"job_title": "Software Engineer", "company": "ABC Company", "requirements": ['skill1', 'skill2']}, {"job_title": "Software Engineer", "company": "ABC Company", "requirements": ['skill3', 'skill4']}]
        self.assertEqual(jobMarketplace.search_jobs("skill6"), [])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
