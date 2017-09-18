from dataAccess import DataAccess
import numpy

class HRLogic:
    def __init__(self):
        self.preferred_schools = ['a']
        self.preferred_employers = ['IBM', '花旗']

    def score_candidates(self):
        dataAccess = DataAccess(subject = 'hr')
        candidates = dataAccess.getAll()
        for candidate in candidates:
            oversea_experience = False
            preferred_employer = False
            score = 50
            candidate['RecentFirm'] = candidate['JobHistory'][0]['Firm'] if len(candidate['JobHistory']) > 0 else '无工作经验'
            avg_hops = 100
            total_months = 0
            count_jobs = 0
            for job_history in candidate['JobHistory']:
                if str(job_history['EndDate']) == 'nan':
                    job_history['EndDate'] = 'Current'
                    job_history['Months'] = 'N/A'
                else:
                    total_months += job_history['Months']
                    count_jobs += 1
                if '海外' in job_history['Position']:
                    oversea_experience = True
                for e in self.preferred_employers:
                    if (job_history['Firm'] in e):
                        preferred_employer = True
            avg_hops = total_months / count_jobs if count_jobs > 0 else 'N/A'
            candidate['AvgHops'] = avg_hops
            # Do not hops for consider candidates who have just graduted.
            if len(candidate['JobHistory']) <= 1:
                avg_hops = 'N/A'
            if avg_hops != 'N/A' and avg_hops < 15:
                score -= 50
            if oversea_experience == True:
                score += 50
            if preferred_employer == True:
                score += 30
            for s in self.preferred_schools:
                if str(candidate['University']) in s:
                    score += 20
            if score < 0:
                score = 0
            if score > 100:
                score = 100
            candidate['reportScore'] = score
            del candidate['Industry']
            del candidate['Position']
            del candidate['ExpectedSalary']
        return candidates[:100]

# hr = HRLogic()
# result = hr.score_candidates()
# print(result[1])