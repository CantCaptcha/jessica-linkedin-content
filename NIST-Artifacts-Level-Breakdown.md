# NIST 800-171 / CMMC Artifact Guide - by Level
_Recommended documents and evidence organized by CMMC Level 1 and Level 2_

**Generated:** 2026-03-31
**Based on:** Steris_Mar_2026_DCG_CMMC_Tracking_v19.xlsx
**Purpose:** Artifact recommendations separated by CMMC level

---

## Overview

| CMMC Level | Controls | Focus |
|-------------|-----------|--------|
| **Level 1** | 17 practices | Basic cyber hygiene - foundational cybersecurity practices |
| **Level 2** | 72 practices | Intermediate protection - documented practices and additional controls |
| **Total** | 110 practices | Full CMMC compliance |

**CMMC Level 2 includes all Level 1 practices** - organizations must implement Level 1 first, then add Level 2 controls.

---

# CMMC LEVEL 1 - Basic Cyber Hygiene

## Level 1 Domains (6)

### Access Control (AC) - 4 Controls

#### AC.1.001 / NIST 3.1.1 - Limit System Access
**Control:** Limit information system access to authorized users, processes acting on behalf of authorized users, or devices.

**Recommended Artifacts:**
- [ ] Active Directory/LDAP user list with account status
- [ ] User access request forms with approval workflows
- [ ] Onboarding checklist with access provisioning steps
- [ ] Account creation/deletion logs (90+ days retention)
- [ ] User account review schedules (quarterly/annual)
- [ ] Role-based access control (RBAC) matrix
- [ ] Access Control Policy (signed and dated)

---

#### AC.1.002 / NIST 3.1.2 - Limit Transactions and Functions
**Control:** Limit system access to types of transactions and functions that authorized users are permitted to execute.

**Recommended Artifacts:**
- [ ] Role-based access control matrix by job function
- [ ] Privilege assignment review documentation
- [ ] Admin access logs with monitoring reports
- [ ] Separation of duties (SoD) matrix
- [ ] User permission audit reports (monthly)

---

#### AC.1.003 / NIST 3.1.3 - Control Flow of CUI
**Control:** Control flow of CUI in accordance with approved authorizations.

**Recommended Artifacts:**
- [ ] Data flow diagrams (DFD)
- [ ] Data classification policy
- [ ] Information transfer procedures
- [ ] Secure transmission protocols documentation (TLS 1.2+, encryption)

---

#### AC.1.004 / NIST 3.1.4 - Separate Duties
**Control:** Separate duties of individuals as appropriate.

**Recommended Artifacts:**
- [ ] Separation of duties matrix
- [ ] Role definitions and responsibilities documentation
- [ ] Conflict of interest policies
- [ ] Approval workflow documentation (dual control)
- [ ] Audit trail for critical transactions

---

### Awareness and Training (AT) - 2 Controls

#### AT.1.001 / NIST 3.2.1 - Ensure Personnel are Trained
**Control:** Ensure that organizational personnel are trained to carry out their assigned information security-related duties and responsibilities.

**Recommended Artifacts:**
- [ ] Security training curriculum
- [ ] Training completion records for all personnel
- [ ] Training schedule and frequency documentation
- [ ] Role-specific training materials
- [ ] Acknowledgement of training policies

---

#### AT.1.002 / NIST 3.2.2 - Ensure Managers Receive Training
**Control:** Ensure that managers of systems are trained to carry out their assigned information security-related duties and responsibilities.

**Recommended Artifacts:**
- [ ] Manager training records
- [ ] Management-level security awareness materials
- [ ] Manager responsibility documentation
- [ ] System owner training certifications

---

### Incident Response (IR) - 1 Control

#### IR.1.001 / NIST 3.6.1 - IR Policy and Procedures
**Control:** Establish and maintain incident response policy and procedures.

**Recommended Artifacts:**
- [ ] Incident response policy (signed and approved)
- [ ] Incident response procedures/playbooks
- [ ] Incident classification matrix
- [ ] Reporting procedures documentation
- [ ] Incident response team (IRT) roster
- [ ] Escalation matrix

---

### Maintenance (MA) - 4 Controls

#### MA.1.001 / NIST 3.7.1 - Maintenance Policy
**Control:** Establish and maintain maintenance policy and procedures.

**Recommended Artifacts:**
- [ ] Maintenance policy
- [ ] Maintenance procedures documentation
- [ ] Maintenance schedule/calendar
- [ ] Maintenance personnel access documentation
- [ ] Vendor maintenance agreements

---

#### MA.1.002 / NIST 3.7.2 - Maintenance Tools
**Control:** Ensure maintenance tools are approved and controlled.

**Recommended Artifacts:**
- [ ] Approved maintenance tools inventory
- [ ] Tool approval process documentation
- [ ] Maintenance tool access controls
- [ ] Tool usage logs
- [ ] Remote maintenance access procedures

---

#### MA.1.003 / NIST 3.7.3 - Maintenance Logs
**Control:** Maintain maintenance logs.

**Recommended Artifacts:**
- [ ] Maintenance log templates
- [ ] Maintenance activity records
- [ ] Log review procedures
- [ ] Scheduled vs. unscheduled maintenance documentation

---

#### MA.1.004 / NIST 3.7.4 - Maintenance Personnel
**Control:** Ensure maintenance personnel are supervised.

**Recommended Artifacts:**
- [ ] Maintenance supervision procedures
- [ ] Personnel background check records
- [ ] Non-disclosure agreements (NDAs)
- [ ] Escort/chaperone procedures
- [ ] Maintenance access logs with supervisor signatures

---

### Media Protection (MP) - 4 Controls

#### MP.1.001 / NIST 3.8.1 - Access to Media
**Control:** Protect CUI on media.

**Recommended Artifacts:**
- [ ] Media access control policy
- [ ] Media inventory (USB drives, external hard drives, etc.)
- [ ] CUI media labeling procedures
- [ ] Media checkout/check-in logs
- [ ] Media destruction procedures

---

#### MP.1.002 / NIST 3.8.2 - Media Sanitization
**Control:** Sanitize media before reuse or release.

**Recommended Artifacts:**
- [ ] Media sanitization policy (NIST SP 800-88)
- [ ] Sanitization procedures documentation
- [ ] Sanitization method inventory (degauss, wipe, shred)
- [ ] Sanitization logs (before release/reuse)
- [ ] Sanitization equipment certification

---

#### MP.1.003 / NIST 3.8.3 - Media Transport
**Control:** Control media transport.

**Recommended Artifacts:**
- [ ] Media transport policy
- [ ] Transport chain-of-custody documentation
- [ ] Encrypted transport procedures
- [ ] Approved carrier agreements
- [ ] Transport logs and receipts

---

#### MP.1.004 / NIST 3.8.4 - Media Marking
**Control:** Mark media with CUI designation and control markings.

**Recommended Artifacts:**
- [ ] CUI marking policy/procedures
- [ ] Control markings guide (CUI, CUI//SP-SIMP, etc.)
- [ ] Marking compliance audit reports
- [ ] Document templates with CUI markings
- [ ] Training materials on CUI markings

---

### Physical Protection (PE) - 2 Controls

#### PE.1.001 / NIST 3.9.1 - Physical Access Policy
**Control:** Establish and maintain physical access policy.

**Recommended Artifacts:**
- [ ] Physical security policy
- [ ] Access control zone documentation
- [ ] Badge access procedures
- [ ] Visitor access procedures
- [ ] Physical access logs (entry/exit)
- [ ] Key/cipher lock control documentation

---

#### PE.1.002 / NIST 3.9.2 - Access Authorization
**Control:** Ensure physical access to CUI is authorized.

**Recommended Artifacts:**
- [ ] Access authorization matrix
- [ ] Badge issuance procedures
- [ ] Temporary access request forms
- [ ] Access revocation procedures
- [ ] Personnel clearance documentation (if applicable)
- [ ] Escort procedures for visitors

---

## Level 1 Summary - Must-Have Artifacts

### Priority Documents (Level 1 Only)
- [ ] **Access Control Policy** (AC.1.001)
- [ ] **User Access Matrix** (AC.1.002, AC.1.004)
- [ ] **Data Flow Diagrams** (AC.1.003)
- [ ] **Security Training Records** - all personnel (AT.1.001)
- [ ] **Manager Training Records** (AT.1.002)
- [ ] **Incident Response Plan** (IR.1.001)
- [ ] **Maintenance Policy** (MA.1.001)
- [ ] **Maintenance Logs** (MA.1.003)
- [ ] **Media Access & Sanitization Policy** (MP.1.001, MP.1.002)
- [ ] **CUI Marking Procedures** (MP.1.004)
- [ ] **Physical Security Policy** (PE.1.001)
- [ ] **Physical Access Logs** (PE.1.002)

---

# CMMC LEVEL 2 - Intermediate Protection

**NOTE:** Level 2 includes ALL Level 1 controls (17 practices) PLUS 55 additional Level 2 practices (72 total)

## Level 2 Domains - Additional Controls

### Access Control (AC) - 1 Additional Control

#### AC.1.005 / NIST 3.1.5 - Least Privilege
**Control:** Employ least privilege principles.

**Recommended Artifacts:**
- [ ] Least privilege policy
- [ ] Just-in-time (JIT) access logs (if applicable)
- [ ] Privilege review schedules and results
- [ ] Temporary elevated access requests
- [ ] Admin account review documentation
- [ ] Access right assignment justification forms
- [ ] Privilege audit reports

---

### Audit and Accountability (AU) - 6 Controls

#### AU.1.001 / NIST 3.3.1 - Create Audit Records
**Control:** Create and retain system audit records to enable monitoring, investigation, analysis, and reporting of unlawful, unauthorized, or inappropriate system activity.

**Recommended Artifacts:**
- [ ] Audit log policy (retention, content, protection)
- [ ] Log management system configuration
- [ ] Audit log samples (login, access, config changes)
- [ ] Log rotation/retention schedules
- [ ] Audit record inventory (what systems log)

---

#### AU.1.002 / NIST 3.3.2 - Enable Auditing
**Control:** Enable audit logging for system components that process CUI.

**Recommended Artifacts:**
- [ ] Audit enablement configuration files
- [ ] System audit policy documentation
- [ ] Logging infrastructure diagram
- [ ] Log source inventory (all CUI-processing systems)
- [ ] Audit control documentation

---

#### AU.1.003 / NIST 3.3.3 - Review Audit Records
**Control:** Review and update audit records.

**Recommended Artifacts:**
- [ ] Audit review schedule and procedures
- [ ] Audit review logs/reports
- [ ] Log analysis reports (automated + manual)
- [ ] Security incident logs correlated with audit data
- [ ] Reviewer training records
- [ ] Escalation procedures for audit anomalies

---

#### AU.1.004 / NIST 3.3.4 - Alert in Case of Audit Failure
**Control:** Alert in the event of an audit logging process failure.

**Recommended Artifacts:**
- [ ] Audit monitoring/alerting configuration
- [ ] Alert contact list
- [ ] Failure response procedures
- [ ] Alert testing records (proof alerts work)
- [ ] Backup logging mechanism documentation

---

#### AU.1.005 / NIST 3.3.5 - Time Synchronization
**Control:** Use internal system clocks to generate time stamps for audit records.

**Recommended Artifacts:**
- [ ] Time synchronization policy (NTP)
- [ ] NTP server configuration documentation
- [ ] Time sync logs
- [ ] Time drift monitoring reports
- [ ] System time settings documentation

---

#### AU.1.006 / NIST 3.3.6 - Protect Audit Information
**Control:** Protect audit information and tools from unauthorized access, modification, or deletion.

**Recommended Artifacts:**
- [ ] Audit data access control policy
- [ ] Audit storage encryption documentation
- [ ] Log access logs (who accessed logs)
- [ ] Audit system backup procedures
- [ ] Write-once/WORM storage configuration
- [ ] Privileged access to audit tools list

---

### Awareness and Training (AT) - 1 Additional Control

#### AT.1.003 / NIST 3.2.3 - Ensure All Personnel Receive Training
**Control:** Ensure that all personnel are trained on cybersecurity and cyber hygiene.

**Recommended Artifacts:**
- [ ] Organization-wide cybersecurity training records
- [ ] Phishing simulation results
- [ ] Security awareness campaign materials
- [ ] Annual security training completion reports
- [ ] Cyber hygiene guidelines and acknowledgments

---

### Configuration Management (CM) - 7 Controls

#### CM.1.001 / NIST 3.4.1 - Baseline Configuration
**Control:** Establish and maintain baseline configurations.

**Recommended Artifacts:**
- [ ] Approved baseline configuration documents
- [ ] Baseline approval signatures
- [ ] Configuration management plan
- [ ] Golden image/repository documentation
- [ ] Baseline version control records
- [ ] Deviation request procedures and logs

---

#### CM.1.002 / NIST 3.4.2 - Track Changes
**Control:** Track, approve, and reject changes to baseline configurations.

**Recommended Artifacts:**
- [ ] Change control policy and procedures
- [ ] Change request forms (CRs)
- [ ] Change advisory board (CAB) meeting minutes
- [ ] Approved/rejected change logs
- [ ] Rollback procedures documentation
- [ ] Emergency change procedures
- [ ] Configuration change audit trails

---

#### CM.1.003 / NIST 3.4.3 - Security Impact Analysis
**Control:** Perform security impact analysis prior to making changes.

**Recommended Artifacts:**
- [ ] Security impact analysis methodology
- [ ] Change risk assessment templates
- [ ] Security impact review logs
- [ ] Stakeholder sign-off for changes
- [ ] Pre- and post-change security testing results
- [ ] Vulnerability scan reports pre/post change

---

#### CM.1.004 / NIST 3.4.4 - Vulnerability Scanning
**Control:** Scan for vulnerabilities and remediate them.

**Recommended Artifacts:**
- [ ] Vulnerability scanning policy and schedule
- [ ] Scan reports (automated and manual)
- [ ] Vulnerability remediation plans
- [ ] Remediation verification reports
- [ ] Exception approval documentation
- [ ] Scanning tool configuration and updates

---

#### CM.1.005 / NIST 3.4.5 - Anti-Malware
**Control:** Employ anti-malware mechanisms.

**Recommended Artifacts:**
- [ ] Anti-malware/EDR deployment records
- [ ] Anti-malware configuration policies
- [ ] Signature/definition update schedules
- [ ] Malware detection logs
- [ ] Malware incident response procedures
- [ ] Exemption documentation (if any systems excluded)

---

#### CM.1.006 / NIST 3.4.6 - Incident Response Testing
**Control:** Perform incident response testing.

**Recommended Artifacts:**
- [ ] Incident response plan (IRP)
- [ ] Incident response test schedules
- [ ] Test scenarios and playbooks
- [ ] Test execution reports (after-action reports)
- [ ] Lessons learned documentation
- [ ] IR plan version control and approvals

---

#### CM.1.007 / NIST 3.4.7 - Emergency Access
**Control:** Establish alternate means of access.

**Recommended Artifacts:**
- [ ] Emergency access procedures
- [ ] Break-glass account documentation
- [ ] Emergency access approval forms
- [ ] Emergency access logs (when used)
- [ ] Emergency access audit reports
- [ ] Emergency contact lists

---

### Identification and Authentication (IA) - 7 Controls

#### IA.1.001 / NIST 3.5.1 - Identify and Authenticate Users
**Control:** Identify and authenticate users to devices and other devices.

**Recommended Artifacts:**
- [ ] Identity and authentication policy
- [ ] Password policy documentation
- [ ] Account lockout/threshold settings
- [ ] Authentication mechanism documentation
- [ ] User identity verification procedures
- [ ] Session timeout configuration
- [ ] Account lockout logs

---

#### IA.1.002 / NIST 3.5.2 - Multi-Factor Authentication
**Control:** Use multi-factor authentication.

**Recommended Artifacts:**
- [ ] MFA policy and scope documentation
- [ ] MFA solution deployment records
- [ ] MFA enforcement configuration
- [ ] Exception approval documentation
- [ ] MFA backup/recovery procedures
- [ ] MFA enrollment/completion reports

---

#### IA.1.003 / NIST 3.5.3 - Device Authentication
**Control:** Verify and control external connections.

**Recommended Artifacts:**
- [ ] External connection inventory
- [ ] VPN access control policies
- [ ] Remote desktop gateway documentation
- [ ] Device authentication certificates
- [ ] Connection approval workflows
- [ ] External system authentication agreements
- [ ] Connection audit logs

---

#### IA.1.004 / NIST 3.5.4 - Replay Protection
**Control:** Employ replay-resistant authentication mechanisms.

**Recommended Artifacts:**
- [ ] Authentication mechanism documentation
- [ ] Replay attack protection configuration
- [ ] Session management policies
- [ ] Token/session expiration settings
- [ ] Authentication protocol specifications

---

#### IA.1.005 / NIST 3.5.5 - Fail-Safe Auth
**Control:** Prevent authentication mechanisms from providing access in fail-safe mode.

**Recommended Artifacts:**
- [ ] Fail-safe authentication documentation
- [ ] Authentication system hardening evidence
- [ ] Backup authentication system configuration
- [ ] Failure mode testing results

---

#### IA.1.006 / NIST 3.5.6 - Token Authenticators
**Control:** Accept only PIV-compliant credentials.

**Recommended Artifacts:**
- [ ] PIV card policy
- [ ] PIV card inventory
- [ ] PIV reader deployment records
- [ ] Smart card management procedures
- [ ] PIV exemption documentation (if applicable)
- [ ] CAC/PIV integration documentation

---

#### IA.1.007 / NIST 3.5.7 - Cryptographic Modules
**Control:** Employ FIPS-validated cryptography.

**Recommended Artifacts:**
- [ ] FIPS-validated module inventory
- [ ] Cryptographic module certificates (FIPS 140-2/140-3)
- [ ] Encryption policy (algorithms, key lengths)
- [ ] Cryptographic module configuration
- [ ] Key management procedures
- [ ] FIPS compliance review reports

---

### Incident Response (IR) - 4 Additional Controls

#### IR.1.002 / NIST 3.6.2 - IR Training
**Control:** Ensure IR personnel are trained.

**Recommended Artifacts:**
- [ ] IR team training records
- [ ] IR training curriculum
- [ ] Certification/training certificates
- [ ] Skill gap analysis documentation
- [ ] Cross-training records

---

#### IR.1.003 / NIST 3.6.3 - IR Testing
**Control:** Test IR capabilities.

**Recommended Artifacts:**
- [ ] IR testing schedule
- [ ] Test scenarios and objectives
- [ ] Test execution reports
- [ ] Tabletop exercise documentation
- [ ] After-action reports (AARs)
- [ ] Lessons learned and improvement plans

---

#### IR.1.004 / NIST 3.6.4 - Incident Monitoring
**Control:** Track and document incidents.

**Recommended Artifacts:**
- [ ] Incident tracking system logs
- [ ] Incident reports (all incidents)
- [ ] Incident timeline documentation
- [ ] Root cause analysis reports
- [ ] Incident closure documentation
- [ ] Trend analysis reports

---

#### IR.1.005 / NIST 3.6.5 - Incident Reporting
**Control:** Ensure incidents are reported.

**Recommended Artifacts:**
- [ ] Incident reporting procedures
- [ ] Reporting channel documentation
- [ ] Awareness campaign materials
- [ ] Anonymous reporting mechanism documentation
- [ ] Reporting acknowledgment receipts
- [ ] Mandatory reporting triggers

---

### Physical Protection (PE) - 4 Additional Controls

#### PE.1.003 / NIST 3.9.3 - Visitor Control
**Control:** Monitor and control physical access.

**Recommended Artifacts:**
- [ ] Visitor management procedures
- [ ] Visitor sign-in/out logs
- [ ] Badge expiration schedules
- [ ] Physical security monitoring reports
- [ ] Lost/stolen badge procedures
- [ ] Badge photo/identification documentation

---

#### PE.1.004 / NIST 3.9.4 - Physical Access Monitoring
**Control:** Physical access to CUI is monitored.

**Recommended Artifacts:**
- [ ] Physical security camera deployment map
- [ ] Access monitoring procedures
- [ ] Alarm/door sensor configuration
- [ ] Physical intrusion logs
- [ ] Security monitoring shift logs
- [ ] Physical incident reports

---

#### PE.1.005 / NIST 3.9.5 - Equipment Maintenance
**Control:** Maintain physical access equipment.

**Recommended Artifacts:**
- [ ] Physical security equipment inventory
- [ ] Equipment maintenance schedule
- [ ] Calibration records (sensors, locks)
- [ ] Equipment testing documentation
- [ ] Replacement/upgrade logs

---

#### PE.1.006 / NIST 3.9.6 - Delivery Areas
**Control:** Control physical access to delivery areas.

**Recommended Artifacts:**
- [ ] Delivery area security procedures
- [ ] Receiving area access controls
- [ ] Package inspection procedures
- [ ] Delivery log documentation
- [ ] Courier/vendor access agreements

---

### Risk Assessment (RA) - 4 Controls

#### RA.1.001 / NIST 3.11.1 - Risk Assessment Policy
**Control:** Establish and maintain risk assessment policy.

**Recommended Artifacts:**
- [ ] Risk management policy
- [ ] Risk assessment methodology
- [ ] Risk tolerance statements
- [ ] Risk assessment schedule
- [ ] Risk register
- [ ] Risk assessment templates

---

#### RA.1.002 / NIST 3.11.2 - Scan for Vulnerabilities
**Control:** Scan CUI systems for vulnerabilities.

**Recommended Artifacts:**
- [ ] Vulnerability scanning policy
- [ ] Scan schedule (quarterly/annual)
- [ ] Vulnerability scan reports
- [ ] False positive documentation
- [ ] Scan tool configuration
- [ ] Scan scope documentation

---

#### RA.1.003 / NIST 3.11.3 - Remediate Vulnerabilities
**Control:** Remediate vulnerabilities.

**Recommended Artifacts:**
- [ ] Vulnerability remediation plan
- [ ] Patch management policy
- [ ] Patch deployment schedules
- [ ] Remediation verification reports
- [ ] Exception approval documentation
- [ ] Risk acceptance documentation

---

#### RA.1.004 / NIST 3.11.4 - Update Risk Assessments
**Control:** Update risk assessments periodically.

**Recommended Artifacts:**
- [ ] Risk assessment update schedule
- [ ] Current risk assessment report
- [ ] Risk review meeting minutes
- [ ] Risk trend analysis
- [ ] Risk acceptance sign-offs
- [ ] Risk committee documentation

---

### Security Assessment (CA) - 8 Controls

#### CA.1.001 / NIST 3.12.1 - Security Assessment Policy
**Control:** Establish and maintain security assessment policy.

**Recommended Artifacts:**
- [ ] Security assessment policy
- [ ] Assessment schedule
- [ ] Assessment team credentials
- [ ] Assessment methodology documentation
- [ ] Third-party assessor agreements (if applicable)
- [ ] Assessment scope documentation

---

#### CA.1.002 / NIST 3.12.2 - Assess Security Controls
**Control:** Assess security controls.

**Recommended Artifacts:**
- [ ] Security control assessment reports
- [ ] Control effectiveness testing results
- [ ] Penetration testing reports
- [ ] Independent assessment documentation
- [ ] Control gap analysis
- [ ] Control testing procedures

---

#### CA.1.003 / NIST 3.12.3 - Remediation Plan
**Control:** Develop and implement remediation plans.

**Recommended Artifacts:**
- [ ] Plan of Action and Milestones (POAM)
- [ ] Gap remediation schedules
- [ ] Remediation responsibility assignments
- [ ] POAM tracking logs
- [ ] Remediation completion evidence
- [ ] POAM status reports

---

#### CA.1.004 / NIST 3.12.4 - System Security Plan
**Control:** Document and monitor security controls in System Security Plan.

**Recommended Artifacts:**
- [ ] System Security Plan (SSP)
- [ ] SSP approval signatures
- [ ] SSP control implementation matrix
- [ ] SSP change control logs
- [ ] SSP distribution records
- [ ] SSP review schedule (annual)
- [ ] SSP version control documentation

---

#### CA.1.005 / NIST 3.12.5 - Update SSP
**Control:** Update SSP to reflect changes.

**Recommended Artifacts:**
- [ ] SSP update procedures
- [ ] SSP change logs
- [ ] SSP version control
- [ ] Update approval documentation
- [ ] SSP review and sign-off records
- [ ] SSP distribution notifications

---

#### CA.1.006 / NIST 3.12.6 - External Connections Review
**Control:** Review and approve external connections.

**Recommended Artifacts:**
- [ ] External connection inventory
- [ ] Connection approval procedures
- [ ] Connection security requirements
- [ ] External connection agreements (MOUs, contracts)
- [ ] Third-party security assessments
- [ ] FedRAMP authorization documents (if applicable)
- [ ] Connection audit logs

---

#### CA.1.007 / NIST 3.12.7 - Continuous Monitoring
**Control:** Establish and monitor configuration settings.

**Recommended Artifacts:**
- [ ] Continuous monitoring plan
- [ ] Monitoring tool inventory
- [ ] Monitoring dashboard/configuration
- [ ] Alert threshold documentation
- [ ] Monitoring logs and reports
- [ ] Security incident correlation rules
- [ ] System health monitoring reports

---

#### CA.1.008 / NIST 3.12.8 - Security Assessments on Change
**Control:** Perform security assessments on changes.

**Recommended Artifacts:**
- [ ] Pre-change security test procedures
- [ ] Post-change security test results
- [ ] Change security impact assessments
- [ ] Regression testing documentation
- [ ] Security testing integration with change management
- [ ] Test environment documentation

---

### System and Communications Protection (SC) - 10 Controls

#### SC.1.001 / NIST 3.13.1 - Boundary Protection
**Control:** Monitor, control, and protect communications.

**Recommended Artifacts:**
- [ ] Network boundary documentation
- [ ] Firewall configuration files
- [ ] Intrusion detection/prevention (IDS/IPS) logs
- [ ] Network segmentation diagrams
- [ ] Border router configurations
- [ ] Network access control lists (ACLs)
- [ ] Traffic flow monitoring reports

---

#### SC.1.002 / NIST 3.13.2 - Information in Transit
**Control:** Protect information in transit.

**Recommended Artifacts:**
- [ ] Encryption-in-transit policy (TLS 1.2+)
- [ ] TLS/SSL configuration documentation
- [ ] Certificate inventory and expiry tracking
- [ ] VPN encryption documentation
- [ ] Secure transmission protocol documentation
- [ ] FIPS-validated cryptographic module certificates

---

#### SC.1.003 / NIST 3.13.3 - Information at Rest
**Control:** Protect information at rest.

**Recommended Artifacts:**
- [ ] Encryption-at-rest policy
- [ ] Full disk encryption deployment records
- [ ] Database encryption configuration
- [ ] File/folder encryption policies
- [ ] Encryption key management procedures
- [ ] FIPS-validated module documentation
- [ ] Storage encryption verification reports

---

#### SC.1.004 / NIST 3.13.4 - CUI Partitioning
**Control:** Separate CUI from non-CUI.

**Recommended Artifacts:**
- [ ] Data partitioning procedures
- [ ] Network segmentation documentation
- [ ] CUI storage location inventory
- [ ] Cross-boundary data flow controls
- [ ] Access control matrix by data classification
- [ ] CUI labeling procedures

---

#### SC.1.005 / NIST 3.13.5 - Denial of Service Protection
**Control:** Employ denial-of-service protection.

**Recommended Artifacts:**
- [ ] DoS/DDoS protection policy
- [ ] DoS mitigation tool configuration
- [ ] Bandwidth monitoring reports
- [ ] DoS response procedures
- [ ] ISP/CDN DDoS protection agreements
- [ ] DoS incident logs

---

#### SC.1.006 / NIST 3.13.6 - Mobile Code Protection
**Control:** Protect against or limit effects of mobile code.

**Recommended Artifacts:**
- [ ] Mobile code policy (Java, ActiveX, etc.)
- [ ] Browser hardening procedures
- [ ] Application allowlist/denylist
- [ ] Code signing verification procedures
- [ ] Sandboxing/isolation documentation
- [ ] Mobile code blocking logs

---

#### SC.1.007 / NIST 3.13.7 - Cryptography Protection
**Control:** Employ cryptography to protect CUI.

**Recommended Artifacts:**
- [ ] Cryptographic standards policy
- [ ] Approved algorithms list (NIST SP 800-52)
- [ ] Encryption strength documentation (key lengths)
- [ ] Key lifecycle management procedures
- [ ] FIPS-validated module inventory
- [ ] Encryption deployment inventory

---

#### SC.1.008 / NIST 3.13.8 - Confidentiality Protection
**Control:** Employ cryptography to protect confidentiality of CUI.

**Recommended Artifacts:**
- [ ] Confidentiality protection policy
- [ ] End-to-end encryption documentation
- [ ] PGP/S/MIME key management
- [ ] Secure email gateway configuration
- [ ] File encryption procedures
- [ ] Secure file transfer protocols (SFTP, etc.)

---

#### SC.1.009 / NIST 3.13.9 - Session Protection
**Control:** Terminate sessions after inactivity.

**Recommended Artifacts:**
- [ ] Session timeout policy
- [ ] Timeout configuration documentation
- [ ] Application timeout settings evidence
- [ ] Session lock enforcement logs
- [ ] Idle session monitoring reports

---

#### SC.1.010 / NIST 3.13.10 - Wireless Access
**Control:** Protect wireless access.

**Recommended Artifacts:**
- [ ] Wireless security policy
- [ ] WPA2/WPA3 Enterprise configuration
- [ ] SSID management documentation
- [ ] Wireless access point inventory
- [ ] Rogue AP detection logs
- [ ] Wireless authentication server configuration (RADIUS)
- [ ] Guest wireless isolation procedures

---

### System and Information Integrity (SI) - 8 Controls

#### SI.1.001 / NIST 3.14.1 - Flaw Remediation
**Control:** Identify, report, and correct system flaws.

**Recommended Artifacts:**
- [ ] Vulnerability management policy
- [ ] Patch management procedures
- [ ] Vulnerability identification logs
- [ ] Patch deployment schedules
- [ ] Flaw remediation tracking
- [ ] Root cause analysis documentation

---

#### SI.1.002 / NIST 3.14.2 - Security Software Updates
**Control:** Update malicious code protection mechanisms.

**Recommended Artifacts:**
- [ ] Anti-malware/EDR update policy
- [ ] Signature update automation configuration
- [ ] Update frequency documentation
- [ ] Update failure notification procedures
- [ ] Anti-malware version inventory
- [ ] Update verification logs

---

#### SI.1.003 / NIST 3.14.3 - Security Baseline Updates
**Control:** Update security baselines.

**Recommended Artifacts:**
- [ ] Security baseline update schedule
- [ ] Baseline version control
- [ ] Baseline approval documentation
- [ ] Update notification procedures
- [ ] Baseline deployment records
- [ ] Configuration drift monitoring reports

---

#### SI.1.004 / NIST 3.14.4 - Security Alerts
**Control:** Monitor system alerts.

**Recommended Artifacts:**
- [ ] Security alert monitoring procedures
- [ ] Alert correlation rules
- [ ] Alert threshold configuration
- [ ] Alert response playbooks
- [ ] SIEM/SOC tool configuration
- [ ] Alert analysis reports
- [ ] False positive documentation

---

#### SI.1.005 / NIST 3.14.5 - Software Flaw Scans
**Control:** Scan for software flaws.

**Recommended Artifacts:**
- [ ] Software scanning policy (SAST/DAST)
- [ ] Static/dynamic analysis scan reports
- [ ] Code review procedures
- [ ] Third-party vulnerability scans
- [ ] Scan frequency documentation
- [ ] Remediation tracking for software flaws

---

#### SI.1.006 / NIST 3.14.6 - Timely Remediation
**Control:** Remediate vulnerabilities in timely manner.

**Recommended Artifacts:**
- [ ] Remediation SLA documentation
- [ ] Vulnerability priority matrix
- [ ] Remediation tracking system logs
- [ ] Overdue vulnerability reports
- [ ] Risk acceptance documentation
- [ ] Remediation delay justifications

---

#### SI.1.007 / NIST 3.14.7 - Unauthorized Software
**Control:** Prohibit unauthorized software.

**Recommended Artifacts:**
- [ ] Software authorization policy
- [ ] Approved software catalog
- [ ] Software deployment procedures
- [ ] Application allowlist configuration
- [ ] Unauthorized software detection logs
- [ ] Software audit reports
- [ ] Shadow IT investigation procedures

---

#### SI.1.008 / NIST 3.14.8 - Security Functionality Verification
**Control:** Verify security functionality.

**Recommended Artifacts:**
- [ ] Security control testing schedule
- [ ] Functionality test reports
- [ ] Control effectiveness validation
- [ ] Security testing methodologies
- [ ] Test environment documentation
- [ ] Third-party validation reports (if applicable)

---

## Level 2 Summary - Must-Have Artifacts (In Addition to Level 1)

### Priority Documents (Level 2 Only)

**Audit & Accountability:**
- [ ] **Audit Log Policy** (AU.1.001, AU.1.002)
- [ ] **Audit Review Procedures** (AU.1.003)
- [ ] **Audit Alerting Configuration** (AU.1.004)
- [ ] **NTP/Time Sync Policy** (AU.1.005)
- [ ] **Audit Data Protection Procedures** (AU.1.006)

**Configuration Management:**
- [ ] **Baseline Configuration Documents** (CM.1.001)
- [ ] **Change Control Procedures** (CM.1.002)
- [ ] **Security Impact Analysis Process** (CM.1.003)
- [ ] **Vulnerability Scanning Policy** (CM.1.004)
- [ ] **Anti-Malware/EDR Policy** (CM.1.005)
- [ ] **IR Testing Schedule** (CM.1.006)
- [ ] **Emergency Access Procedures** (CM.1.007)

**Identification & Authentication:**
- [ ] **MFA Policy** (IA.1.002)
- [ ] **Password Policy** (IA.1.001)
- [ ] **External Connection Procedures** (IA.1.003)
- [ ] **PIV Card Policy** (IA.1.006)
- [ ] **FIPS-Validated Crypto Inventory** (IA.1.007)

**Risk Assessment:**
- [ ] **Risk Management Policy** (RA.1.001)
- [ ] **Vulnerability Scan Reports** (RA.1.002)
- [ ] **Remediation Plan** (RA.1.003)
- [ ] **Risk Review Schedule** (RA.1.004)

**Security Assessment:**
- [ ] **System Security Plan (SSP)** (CA.1.004) - **CRITICAL**
- [ ] **Plan of Action & Milestones (POAM)** (CA.1.003) - **CRITICAL**
- [ ] **Security Assessment Policy** (CA.1.001)
- [ ] **External Connection Inventory** (CA.1.006)
- [ ] **Continuous Monitoring Plan** (CA.1.007)

**System & Communications Protection:**
- [ ] **Encryption-in-Transit Policy** (SC.1.002)
- [ ] **Encryption-at-Rest Policy** (SC.1.003)
- [ ] **Data Partitioning Procedures** (SC.1.004)
- [ ] **Wireless Security Policy** (SC.1.010)
- [ ] **Network Boundary Documentation** (SC.1.001)

**System Integrity:**
- [ ] **Patch Management Policy** (SI.1.001)
- [ ] **Anti-Malware Update Policy** (SI.1.002)
- [ ] **Security Alerting Procedures** (SI.1.004)
- [ ] **Software Authorization Policy** (SI.1.007)

---

# Level Comparison Matrix

| Domain | Level 1 Controls | Level 2 Controls | Total L2 |
|---------|------------------|-------------------|------------|
| **Access Control** | 4 | 5 | 9 |
| **Awareness & Training** | 2 | 3 | 5 |
| **Audit & Accountability** | 0 | 6 | 6 |
| **Configuration Management** | 0 | 7 | 7 |
| **Identification & Auth** | 0 | 7 | 7 |
| **Incident Response** | 1 | 4 | 5 |
| **Maintenance** | 4 | 0 | 4 |
| **Media Protection** | 4 | 0 | 4 |
| **Physical Protection** | 2 | 4 | 6 |
| **Risk Assessment** | 0 | 4 | 4 |
| **Security Assessment** | 0 | 8 | 8 |
| **System & Comms Protection** | 0 | 10 | 10 |
| **System Integrity** | 0 | 8 | 8 |
| **Personnel Security** | 0 | 0 | 0 |
| **TOTAL** | **17** | **72** | **89** |

---

# Implementation Roadmap

## Phase 1: Level 1 Foundation
**Timeline:** 3-6 months
**Controls:** 17 practices

### Quick Wins (Month 1-2)
1. **Policies:** Access Control, Physical Security, Incident Response
2. **Training:** All personnel security training records
3. **Access Control:** User access matrix, role definitions
4. **Physical:** Badge procedures, visitor logs
5. **Media:** Media access and sanitization procedures

### Core Implementation (Month 3-4)
1. **Incident Response:** IR plan, procedures, team roster
2. **Maintenance:** Maintenance policy, logs, procedures
3. **Access Control:** Data flow diagrams, access reviews
4. **Awareness:** Manager training records

### Evidence Collection (Month 5-6)
1. Compile all artifacts for 17 Level 1 controls
2. Conduct internal gap assessment
3. Address any Level 1 gaps
4. Prepare Level 1 evidence package

---

## Phase 2: Level 2 Expansion
**Timeline:** 6-12 months (concurrent with Level 1)
**Controls:** 72 additional practices

### Priority Path (Critical Controls)
1. **System Security Plan (SSP)** - Document all controls
2. **Plan of Action & Milestones (POAM)** - Track gaps
3. **Audit Logging** - Enable and protect audit logs
4. **Multi-Factor Authentication** - Deploy across environment
5. **Configuration Management** - Baselines and change control

### Secondary Controls (Months 3-6)
1. **Vulnerability Management** - Scanning and remediation
2. **Risk Assessment** - Ongoing risk management
3. **Encryption** - In-transit and at-rest
4. **Incident Response** - Testing, tracking, reporting

### Advanced Controls (Months 7-12)
1. **Continuous Monitoring** - SIEM/SOC capabilities
2. **System Integrity** - Patch management, software control
3. **External Connections** - Third-party risk management
4. **Security Assessment** - Ongoing control validation

---

# Artifact Folder Structure by Level

```
CMMC_Evidence/
├── LEVEL_1/
│   ├── AC_Access_Control/
│   │   ├── AC.1.001-3.1.1_2026-03-31_User-Access-Matrix.pdf
│   │   ├── AC.1.002-3.1.2_2026-03-31_RBAC-Matrix.pdf
│   │   ├── AC.1.003-3.1.3_2026-03-31_Data-Flow-Diagram.pdf
│   │   └── AC.1.004-3.1.4_2026-03-31_Separation-of-Duties.pdf
│   ├── AT_Awareness_Training/
│   │   ├── AT.1.001-3.2.1_2026-03-31_Training-Records.pdf
│   │   └── AT.1.002-3.2.2_2026-03-31_Manager-Training.pdf
│   ├── IR_Incident_Response/
│   │   └── IR.1.001-3.6.1_2026-03-31_IR-Plan.pdf
│   ├── MA_Maintenance/
│   │   ├── MA.1.001-3.7.1_2026-03-31_Maintenance-Policy.pdf
│   │   ├── MA.1.003-3.7.3_2026-03-31_Maintenance-Logs.pdf
│   │   └── MA.1.004-3.7.4_2026-03-31_NDA-Records.pdf
│   ├── MP_Media_Protection/
│   │   ├── MP.1.001-3.8.1_2026-03-31_Media-Access-Policy.pdf
│   │   ├── MP.1.002-3.8.2_2026-03-31_Sanitization-Policy.pdf
│   │   ├── MP.1.003-3.8.3_2026-03-31_Transport-Procedures.pdf
│   │   └── MP.1.004-3.8.4_2026-03-31_CUI-Marking-Guide.pdf
│   └── PE_Physical_Protection/
│       ├── PE.1.001-3.9.1_2026-03-31_Physical-Security-Policy.pdf
│       └── PE.1.002-3.9.2_2026-03-31_Authorization-Matrix.pdf
│
└── LEVEL_2/
    ├── AC_Access_Control/
    │   └── AC.1.005-3.1.5_2026-03-31_Least-Privilege-Policy.pdf
    ├── AT_Awareness_Training/
    │   └── AT.1.003-3.2.3_2026-03-31_Cyber-Hygiene-Training.pdf
    ├── AU_Audit_Accountability/
    │   ├── AU.1.001-3.3.1_2026-03-31_Audit-Log-Policy.pdf
    │   ├── AU.1.002-3.3.2_2026-03-31_Audit-Enablement.pdf
    │   ├── AU.1.003-3.3.3_2026-03-31_Audit-Review-Reports.pdf
    │   ├── AU.1.004-3.3.4_2026-03-31_Audit-Alert-Config.pdf
    │   ├── AU.1.005-3.3.5_2026-03-31_NTP-Policy.pdf
    │   └── AU.1.006-3.3.6_2026-03-31_Audit-Protection.pdf
    ├── CM_Configuration_Mgmt/
    │   ├── CM.1.001-3.4.1_2026-03-31_Baseline-Docs.pdf
    │   ├── CM.1.002-3.4.2_2026-03-31_Change-Control.pdf
    │   ├── CM.1.003-3.4.3_2026-03-31_Security-Impact.pdf
    │   ├── CM.1.004-3.4.4_2026-03-31_Vuln-Scans.pdf
    │   ├── CM.1.005-3.4.5_2026-03-31_Anti-Malware-Policy.pdf
    │   ├── CM.1.006-3.4.6_2026-03-31_IR-Test-Reports.pdf
    │   └── CM.1.007-3.4.7_2026-03-31_Emergency-Access.pdf
    ├── IA_Identification_Auth/
    │   ├── IA.1.001-3.5.1_2026-03-31_Password-Policy.pdf
    │   ├── IA.1.002-3.5.2_2026-03-31_MFA-Policy.pdf
    │   ├── IA.1.003-3.5.3_2026-03-31_External-Connections.pdf
    │   ├── IA.1.006-3.5.6_2026-03-31_PIV-Policy.pdf
    │   └── IA.1.007-3.5.7_2026-03-31_FIPS-Crypto-Inventory.pdf
    ├── IR_Incident_Response/
    │   ├── IR.1.002-3.6.2_2026-03-31_IR-Team-Training.pdf
    │   ├── IR.1.003-3.6.3_2026-03-31_IR-Test-Reports.pdf
    │   ├── IR.1.004-3.6.4_2026-03-31_Incident-Tracking.pdf
    │   └── IR.1.005-3.6.5_2026-03-31_Incident-Reporting.pdf
    ├── PE_Physical_Protection/
    │   ├── PE.1.003-3.9.3_2026-03-31_Visitor-Control.pdf
    │   ├── PE.1.004-3.9.4_2026-03-31_Physical-Monitoring.pdf
    │   ├── PE.1.005-3.9.5_2026-03-31_Equipment-Maint.pdf
    │   └── PE.1.006-3.9.6_2026-03-31_Delivery-Area.pdf
    ├── RA_Risk_Assessment/
    │   ├── RA.1.001-3.11.1_2026-03-31_Risk-Policy.pdf
    │   ├── RA.1.002-3.11.2_2026-03-31_Vuln-Scan-Reports.pdf
    │   ├── RA.1.003-3.11.3_2026-03-31_Remediation-Plan.pdf
    │   └── RA.1.004-3.11.4_2026-03-31_Risk-Review.pdf
    ├── CA_Security_Assessment/
    │   ├── CA.1.001-3.12.1_2026-03-31_Security-Assessment-Policy.pdf
    │   ├── CA.1.002-3.12.2_2026-03-31_Control-Assessment.pdf
    │   ├── CA.1.003-3.12.3_2026-03-31_POAM.pdf ⭐ CRITICAL
    │   ├── CA.1.004-3.12.4_2026-03-31_SSP.pdf ⭐ CRITICAL
    │   ├── CA.1.005-3.12.5_2026-03-31_SSP-Update-Procedures.pdf
    │   ├── CA.1.006-3.12.6_2026-03-31_External-Connections.pdf
    │   ├── CA.1.007-3.12.7_2026-03-31_Continuous-Monitoring.pdf
    │   └── CA.1.008-3.12.8_2026-03-31_Change-Assessment.pdf
    ├── SC_System_Comms/
    │   ├── SC.1.001-3.13.1_2026-03-31_Network-Boundary.pdf
    │   ├── SC.1.002-3.13.2_2026-03-31_Encryption-Transit.pdf
    │   ├── SC.1.003-3.13.3_2026-03-31_Encryption-Rest.pdf
    │   ├── SC.1.004-3.13.4_2026-03-31_Data-Partitioning.pdf
    │   ├── SC.1.005-3.13.5_2026-03-31_DoS-Protection.pdf
    │   ├── SC.1.006-3.13.6_2026-03-31_Mobile-Code.pdf
    │   ├── SC.1.007-3.13.7_2026-03-31_Crypto-Standards.pdf
    │   ├── SC.1.008-3.13.8_2026-03-31_Confidentiality.pdf
    │   ├── SC.1.009-3.13.9_2026-03-31_Session-Protection.pdf
    │   └── SC.1.010-3.13.10_2026-03-31_Wireless-Security.pdf
    └── SI_System_Integrity/
        ├── SI.1.001-3.14.1_2026-03-31_Vuln-Mgmt.pdf
        ├── SI.1.002-3.14.2_2026-03-31_AM-Updates.pdf
        ├── SI.1.003-3.14.3_2026-03-31_Baseline-Updates.pdf
        ├── SI.1.004-3.14.4_2026-03-31_Security-Alerts.pdf
        ├── SI.1.005-3.14.5_2026-03-31_Software-Scans.pdf
        ├── SI.1.006-3.14.6_2026-03-31_Timely-Remediation.pdf
        ├── SI.1.007-3.14.7_2026-03-31_Unauthorized-Software.pdf
        └── SI.1.008-3.14.8_2026-03-31_Functionality-Verify.pdf
└── POLICIES/
    ├── Access_Control_Policy.pdf
    ├── Incident_Response_Plan.pdf
    ├── Maintenance_Policy.pdf
    ├── Physical_Security_Policy.pdf
    ├── System_Security_Plan.pdf ⭐ CRITICAL
    └── Plan_of_Action_and_Milestones.pdf ⭐ CRITICAL
```

---

# Quick Reference: Level-Specific Artifact Requirements

| Control Category | Level 1 Required | Level 2 Additional |
|---------------|------------------|---------------------|
| **Policies** | Access Control, Incident Response, Maintenance, Physical Security, Media Protection | Plus: Audit, Config Mgmt, Risk Mgmt, Security Assessment, Encryption, Continuous Monitoring |
| **Procedures** | Incident Response, Maintenance, Media Handling, Physical Access | Plus: Change Control, Patch Mgmt, Vulnerability Scanning, IR Testing, Software Deployment |
| **Technical Evidence** | Access lists, Data flow docs, Training records, Maintenance logs, Media logs | Plus: Audit logs, Config baselines, MFA configs, Encryption certs, Vuln scans, IR tracking |
| **Testing** | N/A | Plus: IR tests, Pen tests, Security assessments, Vulnerability scans |
| **Documentation** | User access matrix, Separation of duties, CUI marking | Plus: SSP, POAM, Risk register, External connection inventory, Software catalog |

---

# Key Takeaways

### Level 1 - "Basic Cyber Hygiene"
- Focus on foundational practices
- Emphasis on policies, access control, and physical security
- 17 practices across 6 domains
- Good starting point for organizations new to compliance

### Level 2 - "Intermediate Protection"
- Builds on Level 1 foundation
- Adds significant technical controls (audit, encryption, MFA, continuous monitoring)
- 72 additional practices across 12 domains
- Requires documented processes and mature security posture
- **Critical Documents:** SSP and POAM are mandatory for Level 2

### Critical Path to Level 2
1. **Start with Level 1** - 3-6 months
2. **Implement SSP** - Documents all controls (L1 + L2)
3. **Create POAM** - Track gaps and remediation
4. **Enable Audit Logging** - Foundation for many Level 2 controls
5. **Deploy MFA** - Key authentication control
6. **Establish Config Management** - Baselines and change control
7. **Build Continuous Monitoring** - SIEM/SOC capabilities

---

**Last Updated:** 2026-03-31
**Source:** Steris_Mar_2026_DCG_CMMC_Tracking_v19.xlsx analysis
**Version:** 2.0 (Level-organized)

---

_Note: This guide separates CMMC Level 1 (17 practices) from Level 2 (72 practices). Level 2 includes all Level 1 requirements. Focus on Level 1 first, then expand to Level 2. Always reference official NIST 800-171A Assessment Objectives for definitive guidance._
