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

class JobMarketplaceTestSubmitResume(unittest.TestCase):
    def test_submit_resume(self):
        jobMarketplace = JobMarketplace()
        jobMarketplace.submit_resume("Tom", ['skill1', 'skill2'], "experience")
        self.assertEqual(jobMarketplace.resumes, [{'name': 'Tom', 'skills': ['skill1', 'skill2'], 'experience': 'experience'}])

    def test_submit_resume_2(self):
        jobMarketplace = JobMarketplace()
        jobMarketplace.submit_resume("Tom", ['skill1', 'skill2'], "experience")
        jobMarketplace.submit_resume("John", ['skill3', 'skill4'], "experience")
        self.assertEqual(jobMarketplace.resumes, [{'name': 'Tom', 'skills': ['skill1', 'skill2'], 'experience': 'experience'}, {'name': 'John', 'skills': ['skill3', 'skill4'], 'experience': 'experience'}])

    def test_submit_resume_3(self):
        jobMarketplace = JobMarketplace()
        jobMarketplace.submit_resume("Tom", ['skill1', 'skill2'], "experience")
        jobMarketplace.submit_resume("John", ['skill3', 'skill4'], "experience")
        jobMarketplace.submit_resume("Tom", ['skill1', 'skill2'], "experience")
        self.assertEqual(jobMarketplace.resumes, [{'name': 'Tom', 'skills': ['skill1', 'skill2'], 'experience': 'experience'}, {'name': 'John', 'skills': ['skill3', 'skill4'], 'experience': 'experience'}, {'name': 'Tom', 'skills': ['skill1', 'skill2'], 'experience': 'experience'}])

    def test_submit_resume_4(self):
        jobMarketplace = JobMarketplace()
        jobMarketplace.submit_resume("Tom", ['skill1', 'skill2'], "experience")
        jobMarketplace.submit_resume("John", ['skill3', 'skill4'], "experience")
        jobMarketplace.submit_resume("Tom", ['skill1', 'skill2'], "experience")
        jobMarketplace.submit_resume("John", ['skill3', 'skill4'], "experience")
        self.assertEqual(jobMarketplace.resumes, [{'name': 'Tom', 'skills': ['skill1', 'skill2'], 'experience': 'experience'}, {'name': 'John', 'skills': ['skill3', 'skill4'], 'experience': 'experience'}, {'name': 'Tom', 'skills': ['skill1', 'skill2'], 'experience': 'experience'}, {'name': 'John', 'skills': ['skill3', 'skill4'], 'experience': 'experience'}])

    def test_submit_resume_5(self):
        jobMarketplace = JobMarketplace()
        jobMarketplace.submit_resume("Tom", ['skill1', 'skill2'], "experience")
        jobMarketplace.submit_resume("John", ['skill3', 'skill4'], "experience")
        jobMarketplace.submit_resume("Tom", ['skill1', 'skill2'], "experience")
        jobMarketplace.submit_resume("John", ['skill3', 'skill4'], "experience")
        jobMarketplace.submit_resume("Tom", ['skill1', 'skill2'], "experience")
        self.assertEqual(jobMarketplace.resumes, [{'name': 'Tom', 'skills': ['skill1', 'skill2'], 'experience': 'experience'}, {'name': 'John', 'skills': ['skill3', 'skill4'], 'experience': 'experience'}, {'name': 'Tom', 'skills': ['skill1', 'skill2'], 'experience': 'experience'}, {'name': 'John', 'skills': ['skill3', 'skill4'], 'experience': 'experience'}, {'name': 'Tom', 'skills': ['skill1', 'skill2'], 'experience': 'experience'}])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
