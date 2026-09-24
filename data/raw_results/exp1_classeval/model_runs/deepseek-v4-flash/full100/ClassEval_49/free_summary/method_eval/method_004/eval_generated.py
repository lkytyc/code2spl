class JobMarketplace:
    def __init__(self):
        self.job_listings = []
        self.resumes = []

    def post_job(self, title, company, required_skills):
        self.job_listings.append({
            'title': title,
            'company': company,
            'required_skills': required_skills
        })

    def remove_job(self, job):
        self.job_listings.remove(job)

    def submit_resume(self, name, skills, experience):
        self.resumes.append({
            'name': name,
            'skills': skills,
            'experience': experience
        })

    def withdraw_resume(self, resume):
        self.resumes.remove(resume)

    def search_jobs(self, criteria):
        criteria = criteria.lower()
        return [
            job for job in self.job_listings
            if criteria in job['title'].lower()
            or any(criteria in skill.lower() for skill in job['required_skills'])
        ]

    def get_job_applicants(self, job):
        return [
            resume for resume in self.resumes
            if self.matches_requirements(resume['skills'], job['required_skills'])
        ]

    @staticmethod
    def matches_requirements(skills, requirements):
        return all(skill in requirements for skill in skills)

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
