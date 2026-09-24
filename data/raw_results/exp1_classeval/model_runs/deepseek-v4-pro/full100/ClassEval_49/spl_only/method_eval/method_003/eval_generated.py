class JobMarketplace:
    def __init__(self):
        self.job_listings = []
        self.resumes = []

    def post_job(self, job_title, company, requirements):
        job = {
            "job_title": job_title,
            "company": company,
            "requirements": requirements
        }
        self.job_listings.append(job)

    def remove_job(self, job):
        self.job_listings.remove(job)

    def submit_resume(self, name, skills, experience):
        resume = {
            "name": name,
            "skills": skills,
            "experience": experience
        }
        self.resumes.append(resume)

    def withdraw_resume(self, resume):
        self.resumes.remove(resume)

    def search_jobs(self, criteria):
        matching_jobs = []
        criteria_lower = criteria.lower()
        for job_listing in self.job_listings:
            title_match = criteria_lower in job_listing["job_title"].lower()
            requirements_match = criteria_lower in [req.lower() for req in job_listing["requirements"]]
            if title_match or requirements_match:
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

class JobMarketplaceTestWithdrawResume(unittest.TestCase):
    def test_withdraw_resume(self):
        jobMarketplace = JobMarketplace()
        jobMarketplace.resumes = [{"name": "Tom", "skills": ['skill1', 'skill2'], "experience": "experience"}]
        jobMarketplace.withdraw_resume(jobMarketplace.resumes[0])
        self.assertEqual(jobMarketplace.resumes, [])

    def test_withdraw_resume_2(self):
        jobMarketplace = JobMarketplace()
        jobMarketplace.resumes = [{"name": "Tom", "skills": ['skill1', 'skill2'], "experience": "experience"}, {"name": "John", "skills": ['skill3', 'skill4'], "experience": "experience"}]
        jobMarketplace.withdraw_resume(jobMarketplace.resumes[0])
        self.assertEqual(jobMarketplace.resumes, [{'name': 'John', 'skills': ['skill3', 'skill4'], 'experience': 'experience'}])

    def test_withdraw_resume_3(self):
        jobMarketplace = JobMarketplace()
        jobMarketplace.resumes = [{"name": "Tom", "skills": ['skill1', 'skill2'], "experience": "experience"}, {"name": "John", "skills": ['skill3', 'skill4'], "experience": "experience"}]
        jobMarketplace.withdraw_resume(jobMarketplace.resumes[0])
        jobMarketplace.withdraw_resume(jobMarketplace.resumes[0])
        self.assertEqual(jobMarketplace.resumes, [])
    
    def test_withdraw_resume_4(self):
        jobMarketplace = JobMarketplace()
        jobMarketplace.resumes = [{"name": "Amy", "skills": ['skill3', 'skill2'], "experience": "experience"}, {"name": "John", "skills": ['skill3', 'skill4'], "experience": "experience"}]
        jobMarketplace.withdraw_resume(jobMarketplace.resumes[0])
        jobMarketplace.withdraw_resume(jobMarketplace.resumes[0])
        self.assertEqual(jobMarketplace.resumes, [])

    def test_withdraw_resume_5(self):
        jobMarketplace = JobMarketplace()
        jobMarketplace.resumes = [{"name": "Amy", "skills": ['skill1', 'skill2'], "experience": "experience"}, {"name": "John", "skills": ['skill3', 'skill4'], "experience": "experience"}]
        jobMarketplace.withdraw_resume(jobMarketplace.resumes[0])
        self.assertEqual(jobMarketplace.resumes, [{'experience': 'experience', 'name': 'John', 'skills': ['skill3', 'skill4']}])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
