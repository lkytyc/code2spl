class JobMarketplace:
    def __init__(self):
        self.jobs = []
        self.resumes = []

    def post_job(self, job_title, company, requirements):
        job = {
            "job_title": job_title,
            "company": company,
            "requirements": list(requirements),
        }
        self.jobs.append(job)
        return job

    def remove_job(self, job):
        self.jobs.remove(job)

    def submit_resume(self, name, skills, experience):
        resume = {
            "name": name,
            "skills": list(skills),
            "experience": experience,
        }
        self.resumes.append(resume)
        return resume

    def withdraw_resume(self, resume):
        self.resumes.remove(resume)

    def search_jobs(self, criteria):
        criteria_lower = str(criteria).lower()
        results = []
        for job in self.jobs:
            title_match = criteria_lower in str(job.get("job_title", "")).lower()
            requirements_match = any(
                criteria_lower in str(req).lower() for req in job.get("requirements", [])
            )
            if title_match or requirements_match:
                results.append(job)
        return results

    def get_job_applicants(self, job):
        requirements = job.get("requirements", [])
        return [resume for resume in self.resumes if self.matches_requirements(resume, requirements)]

    @staticmethod
    def matches_requirements(resume, requirements):
        requirements_set = set(requirements)
        for skill in resume.get("skills", []):
            if skill not in requirements_set:
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
