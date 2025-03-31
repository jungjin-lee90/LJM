from crawler.wanted import get_wanted_jobs
from crawler.rocketpunch import get_rocketpunch_jobs
from crawler.saramin import get_saramin_jobs
from crawler.jobkorea import get_jobkorea_jobs

def get_all_jobs(keyword: str) -> list:
    jobs = []

#    try:
#        jobs += get_wanted_jobs(keyword)
#    except Exception as e:
#        print("[원티드 수집 실패]", e)

#    try:
#        jobs += get_rocketpunch_jobs(keyword)
#    except Exception as e:
#        print("[로켓펀치 수집 실패]", e)

#    try:
#        jobs += get_saramin_jobs(keyword)
#    except Exception as e:
#        print("[사람인 수집 실패]", e)

    try:
        jobs += get_jobkorea_jobs(keyword)
    except Exception as e:
        print("[잡코리아 수집 실패]", e)

    return jobs
