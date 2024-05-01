import email
import dns.resolver
from ipwhois import IPWhois
from urllib.parse import urlparse
from ipwhois.exceptions import ASNRegistryError
import hashlib
import re

def parse_email_headers(file_path):
    with open(file_path, 'r') as f:
        msg = email.message_from_file(f)
    
    headers = {}
    for key in msg.keys():
        headers[key.lower()] = msg[key]
    
    return headers

def analyze_ip(ip_address):
    try:
        ip_info = IPWhois(ip_address).lookup_rdap()
        return ip_info
    except ASNRegistryError:
        return "ASN information not available for this IP address."

def analyze_url(url):
    parsed_url = urlparse(url)
    return parsed_url

def calculate_hash(data):
    md5_hash = hashlib.md5(data.encode()).hexdigest()
    sha1_hash = hashlib.sha1(data.encode()).hexdigest()
    sha256_hash = hashlib.sha256(data.encode()).hexdigest()
    return md5_hash, sha1_hash, sha256_hash

def check_mx_records(domain):
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        mx_list = [str(mx.exchange) for mx in mx_records]
        return mx_list
    except dns.resolver.NoAnswer:
        return []

def check_txt_record(domain, record_type):
    try:
        txt_records = dns.resolver.resolve(domain, record_type)
        txt_list = [str(txt) for txt in txt_records]
        return txt_list
    except dns.resolver.NXDOMAIN:
        return []

def check_spf_dkim_dmarc(domain):
    spf_records = check_txt_record(domain, 'TXT')
    spf_records = [record for record in spf_records if 'spf' in record.lower()]

    dkim_selector = 'default'  # Change this to your DKIM selector if necessary
    dkim_domain = f"{dkim_selector}._domainkey.{domain}"
    dkim_records = check_txt_record(dkim_domain, 'TXT')

    dmarc_domain = '_dmarc.' + domain
    dmarc_records = check_txt_record(dmarc_domain, 'TXT')

    return spf_records, dkim_records, dmarc_records

def print_two_columns(key, value):
    print(f"{key:<25}: {value}")

def main():
    file_path = input("Enter the path to the email headers file: ")
    headers = parse_email_headers(file_path)
    print("Email Headers:")
    for key, value in headers.items():
        print_two_columns(key, value)
    
    if 'received' in headers:
        ip_pattern = re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b")
        match = ip_pattern.search(headers['received'])
        if match:
            ip_address = match.group()
            ip_info = analyze_ip(ip_address)
            print_two_columns("IP Address Information", ip_info)
        else:
            print("IP address not found in 'Received' header.")

    if 'from' in headers:
        sender_email = headers['from'].split(' ')[-1].strip('<>')
        sender_url_info = analyze_url(sender_email)
        print_two_columns("Sender Email Information", sender_url_info)
        sender_domain = sender_email.split('@')[-1]
        
        # Check MX records
        mx_records = check_mx_records(sender_domain)
        if mx_records:
            print("MX Records:")
            for mx_record in mx_records:
                print(mx_record)
        else:
            print("No MX records found for the sender's domain.")
        
        # Check SPF, DKIM, and DMARC records
        spf_records, dkim_records, dmarc_records = check_spf_dkim_dmarc(sender_domain)
        if spf_records:
            print("SPF Records:")
            for spf_record in spf_records:
                print(spf_record)
        else:
            print("No SPF records found for the sender's domain.")
        
        if dkim_records:
            print("DKIM Records:")
            for dkim_record in dkim_records:
                print(dkim_record)
        else:
            print("No DKIM records found for the sender's domain.")

        if dmarc_records:
            print("DMARC Records:")
            for dmarc_record in dmarc_records:
                print(dmarc_record)
        else:
            print("No DMARC records found for the sender's domain.")

if __name__ == "__main__":
    main()
