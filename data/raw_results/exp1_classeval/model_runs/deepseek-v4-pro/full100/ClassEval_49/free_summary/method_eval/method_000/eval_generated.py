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
