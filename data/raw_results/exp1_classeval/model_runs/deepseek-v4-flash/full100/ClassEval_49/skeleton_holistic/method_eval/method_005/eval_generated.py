class JobMarketplace:
    def __init__(self):
        self.job_listings = []
        self.resumes = []

    def post_job(self, job_title, company, requirements):
        self.job_listings.append({
            "job_title": job_title,
            "company": company,
            "requirements": requirements
        })

    def remove_job(self, job):
        self.job_listings.remove(job)

    def submit_resume(self, name, skills, experience):
        self.resumes.append({
            "name": name,
            "skills": skills,
            "experience": experience
        })

    def withdraw_resume(self, resume):
        self.resumes.remove(resume)

    def search_jobs(self, criteria):
        return [job for job in self.job_listings if criteria in job["requirements"]]

    def matches_requirements(self, resume, job):
        return all(skill in resume["skills"] for skill in job["requirements"])

    def get_job_applicants(self, job):
        return [resume for resume in self.resumes if self.matches_requirements(resume, job)]

import unittest

class JobMarketplaceTestGetJobApplicants(unittest.TestCase):
    def test_get_job_applicants(self):
        jobMarketplace = JobMarketplace()
        jobMarketplace.resumes = [{"name": "Tom", "skills": ['skill1', 'skill2'], "experience": "experience"}]
        jobMarketplace.job_listings = [{"job_title": "Software Engineer", "company": "ABC Company", "requirements": ['skill1', 'skill2']}]
        self.assertEqual(jobMarketplace.get_job_applicants(jobMarketplace.job_listings[0]), [{'name': 'Tom', 'skills': ['skill1', 'skill2'], 'experience': 'experience'}])

    def test_get_job_applicants_2(self):
        jobMarketplace = JobMarketplace()
        jobMarketplace.resumes = [{"name": "Tom", "skills": ['skill1', 'skill2'], "experience": "experience"}, {"name": "John", "skills": ['skill3', 'skill4'], "experience": "experience"}]
        jobMarketplace.job_listings = [{"job_title": "Software Engineer", "company": "ABC Company", "requirements": ['skill1', 'skill2']}]
        self.assertEqual(jobMarketplace.get_job_applicants(jobMarketplace.job_listings[0]), [{'name': 'Tom', 'skills': ['skill1', 'skill2'], 'experience': 'experience'}])

    def test_get_job_applicants_3(self):
        jobMarketplace = JobMarketplace()
        jobMarketplace.resumes = [{"name": "Tom", "skills": ['skill1', 'skill2'], "experience": "experience"}, {"name": "John", "skills": ['skill3', 'skill4'], "experience": "experience"}]
        jobMarketplace.job_listings = [{"job_title": "Software Engineer", "company": "ABC Company", "requirements": ['skill3', 'skill4']}]
        self.assertEqual(jobMarketplace.get_job_applicants(jobMarketplace.job_listings[0]), [{'name': 'John', 'skills': ['skill3', 'skill4'], 'experience': 'experience'}])

    def test_get_job_applicants_4(self):
        jobMarketplace = JobMarketplace()
        jobMarketplace.resumes = [{"name": "Tom", "skills": ['skill1', 'skill2'], "experience": "experience"}, {"name": "John", "skills": ['skill3', 'skill4'], "experience": "experience"}]
        jobMarketplace.job_listings = [{"job_title": "Software Engineer", "company": "ABC Company", "requirements": ['skill5', 'skill6']}]
        self.assertEqual(jobMarketplace.get_job_applicants(jobMarketplace.job_listings[0]), [])

    def test_get_job_applicants_5(self):
        jobMarketplace = JobMarketplace()
        jobMarketplace.resumes = [{"name": "Tom", "skills": ['skill1', 'skill2'], "experience": "experience"}, {"name": "John", "skills": ['skill3', 'skill4'], "experience": "experience"}]
        jobMarketplace.job_listings = [{"job_title": "Software Engineer", "company": "ABC Company", "requirements": ['skill6', 'skill7']}]
        self.assertEqual(jobMarketplace.get_job_applicants(jobMarketplace.job_listings[0]), [])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
