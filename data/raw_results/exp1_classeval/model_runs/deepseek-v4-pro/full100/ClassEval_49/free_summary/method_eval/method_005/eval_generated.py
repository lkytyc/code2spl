class JobMarketplace:
    def __init__(self):
        self.job_listings = {}
        self.resumes = {}

    def post_job(self, job_title, company, requirements):
        job_id = len(self.job_listings) + 1
        self.job_listings[job_id] = {
            'title': job_title,
            'company': company,
            'requirements': set(requirements)
        }
        return job_id

    def remove_job(self, job_id):
        if job_id in self.job_listings:
            del self.job_listings[job_id]

    def submit_resume(self, name, skills):
        resume_id = len(self.resumes) + 1
        self.resumes[resume_id] = {
            'name': name,
            'skills': set(skills)
        }
        return resume_id

    def withdraw_resume(self, resume_id):
        if resume_id in self.resumes:
            del self.resumes[resume_id]

    def search_jobs(self, search_term):
        results = []
        for job_id, job in self.job_listings.items():
            if search_term.lower() in job['title'].lower() or search_term.lower() in job['company'].lower():
                results.append(job_id)
        return results

    def search_jobs_by_requirements(self, required_skills):
        required_skills = set(required_skills)
        results = []
        for job_id, job in self.job_listings.items():
            if required_skills.issubset(job['requirements']):
                results.append(job_id)
        return results

    def get_applicants(self, job_id):
        if job_id not in self.job_listings:
            return []
        job_requirements = self.job_listings[job_id]['requirements']
        applicants = []
        for resume_id, resume in self.resumes.items():
            if resume['skills'].issubset(job_requirements):
                applicants.append(resume_id)
        return applicants

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
