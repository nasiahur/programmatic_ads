import json
import argparse
import logging
import os
import traceback

reportLabExists = True

try:
    from user_report import *
    from domain_report import *
    from ip_report import *
    from category_report import *
    from policy_report import *
    from bandwidth_date_report import *
    from bandwidth_hour_report import *
    from search_queries_report import *
    from squid_bandwidth_report import *
    from squid_domain_report import *
    from squid_user_report import *
    from youtube_report import *

except ImportError:
    reportLabExists = False

def valid_pdf_install():
    return reportLabExists

def generate_pdf_report(dir):
    # create logger
    logger = logging.getLogger(dir)
    logger.setLevel(logging.INFO)

    # create file handler
    fh = logging.FileHandler(filename=os.path.join(dir, 'data', 'pdf.log'))
    fh.setLevel(logging.INFO)

    # create formatter
    formatter = logging.Formatter('%(asctime)s %(message)s')
    fh.setFormatter(formatter)

    logger.addHandler(fh)

    try:
        # generate the report
        with open(os.path.join(dir, 'data', 'meta.json')) as meta_file:
            meta = json.load(meta_file)

        reports = {
            "icap-users-top-by-requests": TopUserByRequests(dir, "hits"),
            "icap-users-top-by-bandwidth": TopUserByBandwidth(dir, "size"),
            "icap-users-top-by-domains": TopUserByDomains(dir, "domains"),
            "icap-users-detailed-by-domains":TopUserByDomains(dir, "domains"),
            "icap-users-top-blocked-by-domains":TopUserByBlockedDomains(dir, "domains"),
            "icap-users-top-unproductive-by-domains":TopUserByBlockedDomains(dir, "domains"),
            "icap-users-detailed-blocked-by-domains":TopUserByBlockedDomains(dir, "domains"),
            "icap-users-detailed-unproductive-by-domains":TopUserByBlockedDomains(dir, "domains"),
            "icap-domains-top-by-bandwidth": TopDomainByBandwidth(dir, "size"),
            "icap-domains-top-by-requests": TopDomainByRequests(dir, "hits"),
            "icap-domains-top-by-users": TopDomainByUsers(dir, "users"),
            "icap-domains-top-by-ips": TopDomainByIps(dir, "ips"),
            "icap-domains-top-blocked-by-bandwidth": TopDomainByBandwidth(dir, "size"),
            "icap-domains-top-blocked-by-requests": TopBlockedDomainsByRequests(dir, "hits"),
            "icap-domains-top-blocked-by-users": TopDomainByUsers(dir, "users"),
            "icap-domains-top-blocked-by-ips": TopDomainByIps(dir, "ips"),
            "icap-domains-top-unproductive-by-bandwidth": TopDomainByBandwidth(dir, "size"),
            "icap-domains-top-unproductive-by-users": TopDomainByUsers(dir, "users"),
            "icap-domains-top-unproductive-by-requests": TopBlockedDomainsByRequests(dir, "hits"),
            "icap-domains-top-unproductive-by-ips": TopDomainByIps(dir, "ips"),
            "icap-domains-detailed": TopDomainByBandwidth(dir, "size"),
            "icap-ips-top-by-bandwidth": TopIpByBandwidth(dir, "size"),
            "icap-ips-top-by-requests": TopIpByRequests(dir, "hits"),
            "icap-ips-top-by-domains": TopIpByDomains(dir, "domains"),
            "icap-ips-top-blocked-by-domains": TopIpByBlockedDomains(dir, "domains"),
            "icap-ips-top-unproductive-by-domains": TopIpByBlockedDomains(dir, "domains"),
            "icap-ips-detailed-by-domains": TopIpByBlockedDomains(dir, "domains"),
            "icap-ips-detailed-blocked-by-domains": TopIpByBlockedDomains(dir, "domains"),
            "icap-ips-detailed-unproductive-by-domains": TopIpByBlockedDomains(dir, "domains"),
            "icap-categories-top-by-requests": TopCategoryByRequests(dir, "hits"),
            "icap-categories-top-by-bandwidth": TopCategoryByBandwidth(dir, "size"),
            "icap-categories-top-by-users": TopCategoryByUsers(dir, "users"),
            "icap-categories-top-by-ips": TopCategoryByIps(dir, "ips"),
            "icap-categories-detailed": TopCategoryByBandwidth(dir, "size"),
            "icap-policies-top-by-bandwidth": TopPolicyByBandwidth(dir, "size"),
            "icap-policies-top-by-requests": TopPolicyByRequests(dir, "hits"),
            "icap-policies-top-by-users": TopPolicyByUsers(dir, "users"),
            "icap-policies-top-by-ips": TopPolicyByIps(dir, "ips"),
            "icap-dates-by-bandwidth": TopBandwidthByDate(dir, "size"),
            "icap-dates-detailed-by-bandwidth": TopBandwidthByDate(dir, "size"),
            "icap-hours-by-bandwidth": TopBandwidthByHour(dir, "size"),
            "icap-hours-detailed-by-bandwidth": TopBandwidthByHour(dir, "size"),
            "icap-users-search-queries": UserSearchQueriesReport(dir, ""),
            "icap-users-youtube": YoutubeReport(dir, ""),
            "squid-bandwidth": SquidBandwidthByDate(dir, "size"),
            "squid-user-activities": SquidUserByBandwidth(dir, "size"),
            "squid-denied-requests": SquidUserByBandwidth(dir, "size"),
            "squid-unauthenticated-requests": SquidUserByBandwidth(dir, "size"),
            "squid-top-domains": SquidDomainByBandwidth(dir, "size"),
        }

        if meta["template"] not in reports:
            logger.error("Unsupported report type '%s'", meta["template"])
            logger.removeHandler(fh)
            fh.close()
            return False

        reports[meta["template"]].build()
        logger.removeHandler(fh)
        fh.close()
        return True

    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())

    logger.removeHandler(fh)
    fh.close()
    return False

#
# main
#
def main():
    # define arguments
    parser = argparse.ArgumentParser(description='Generates a pdf report given a directory')
    parser.add_argument("--reportdir", help="Report directory", required=True)

    # parse them
    args = parser.parse_args()

    # enable logging
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
    generate_pdf_report(args.reportdir)
    logging.info("Pdf generated successfully")

if __name__ == '__main__':
    main()
