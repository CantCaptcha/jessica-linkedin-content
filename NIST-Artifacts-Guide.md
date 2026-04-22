# NIST 800-171 / CMMC Artifact Guide
_Recommended documents and evidence for each control and assessment objective_

**Generated:** 2026-03-31
**Based on:** Steris_Mar_2026_DCG_CMMC_Tracking_v19.xlsx
**Purpose:** Comprehensive artifact recommendations for CMMC/NIST 800-171 compliance

---

## Artifact Naming Convention

**Standard Format:** `<ORG>_<Control-ID>_<Date>_<Description>`

**Examples:**
- `DCG_3.1.1[a]_2026-03-31_AD-User-Snapshot.pdf`
- `DCG_RA.3.11.1_2026-03-31_Risk-Assessment.pdf`
- `DCG_AC.1.001_2026-03-31_Access-Control-Policy.docx`

---

## Domain 1: Access Control (AC)

### AC.1.001 / NIST 3.1.1 - Limit System Access
**Control:** Limit information system access to authorized users, processes acting on behalf of authorized users, or devices.

**Assessment Objective [a]**: Authorized users are identified

**Recommended Artifacts:**
- [ ] Active Directory/LDAP user list with account status (enabled/disabled)
- [ ] User access request forms with approval workflows
- [ ] Onboarding checklist with access provisioning steps
- [ ] Account creation/deletion logs (90+ days retention)
- [ ] User account review schedules (quarterly/annual)
- [ ] Role-based access control (RBAC) matrix
- [ ] MFA enrollment records (if applicable)
- [ ] Access Control Policy (signed and dated)

**Assessment Objective [b]**: Processes acting on behalf of authorized users are identified

**Recommended Artifacts:**
- [ ] Service account inventory with ownership
- [ ] Service account access request procedures
- [ ] Automated process/service documentation
- [ ] API key management records
- [ ] Scheduled task/automation inventory
- [ ] Process authentication mechanisms documentation
- [ ] Third-party service account agreements

**Assessment Objective [c]**: Devices (and other systems) authorized to connect to system are identified

**Recommended Artifacts:**
- [ ] Network device inventory (switches, routers, firewalls)
- [ ] MAC address filter lists
- [ ] NAC (Network Access Control) policies
- [ ] Authorized device registry
- [ ] BYOD policy (if applicable)
- [ ] Guest network documentation
- [ ] Device certificate inventory
- [ ] Firewall access control lists (ACLs)

---

### AC.1.002 / NIST 3.1.2 - Limit Transactions and Functions
**Control:** Limit system access to the types of transactions and functions that authorized users are permitted to execute.

**Recommended Artifacts:**
- [ ] Role-based access control matrix by job function
- [ ] Privilege assignment review documentation
- [ ] Admin access logs with monitoring reports
- [ ] Separation of duties (SoD) matrix
- [ ] User permission audit reports (monthly)
- [ ] Application access control configurations
- [ ] Privileged access management (PAM) system logs
- [ ] Application function approval workflows

---

### AC.1.003 / NIST 3.1.3 - Control Flow of CUI
**Control:** Control the flow of CUI in accordance with approved authorizations.

**Recommended Artifacts:**
- [ ] Data flow diagrams (DFD)
- [ ] Data classification policy
- [ ] Information transfer procedures
- [ ] Secure transmission protocols documentation (TLS 1.2+, encryption)
- [ ] Data flow control matrices
- [ ] Cross-domain solution configurations (if applicable)
- [ ] External transfer approval logs
- [ ] Network segmentation diagrams

---

### AC.1.004 / NIST 3.1.4 - Separate Duties
**Control:** Separate duties of individuals as appropriate.

**Recommended Artifacts:**
- [ ] Separation of duties matrix
- [ ] Role definitions and responsibilities documentation
- [ ] Conflict of interest policies
- [ ] Approval workflow documentation (dual control)
- [ ] Privilege segregation evidence
- [ ] Audit trail for critical transactions

---

### AC.1.005 / NIST 3.1.5 - Least Privilege
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

## Domain 2: Awareness and Training (AT)

### AT.1.001 / NIST 3.2.1 - Ensure Personnel are Trained
**Control:** Ensure that organizational personnel are trained to carry out their assigned information security-related duties and responsibilities.

**Recommended Artifacts:**
- [ ] Security training curriculum
- [ ] Training completion records for all personnel
- [ ] Training schedule and frequency documentation
- [ ] Role-specific training materials
- [ ] Acknowledgement of training policies
- [ ] Training effectiveness assessments/quizzes
- [ ] New hire security orientation checklists

---

### AT.1.002 / NIST 3.2.2 - Ensure Managers Receive Training
**Control:** Ensure that managers of systems are trained to carry out their assigned information security-related duties and responsibilities.

**Recommended Artifacts:**
- [ ] Manager training records
- [ ] Management-level security awareness materials
- [ ] Manager responsibility documentation
- [ ] System owner training certifications
- [ ] Leadership security briefings attendance

---

### AT.1.003 / NIST 3.2.3 - Ensure All Personnel Receive Training
**Control:** Ensure that all personnel are trained on cybersecurity and cyber hygiene.

**Recommended Artifacts:**
- [ ] Organization-wide cybersecurity training records
- [ ] Phishing simulation results
- [ ] Security awareness campaign materials
- [ ] Annual security training completion reports
- [ ] Cyber hygiene guidelines and acknowledgments
- [ ] Training reminder notifications

---

## Domain 3: Audit and Accountability (AU)

### AU.1.001 / NIST 3.3.1 - Create Audit Records
**Control:** Create and retain system audit records to the extent needed to enable the monitoring, investigation, analysis, and reporting of unlawful, unauthorized, or other inappropriate system activity.

**Recommended Artifacts:**
- [ ] Audit log policy (retention, content, protection)
- [ ] Log management system configuration
- [ ] Audit log samples (login, access, config changes)
- [ ] Log rotation/retention schedules
- [ ] Audit record inventory (what systems log)
- [ ] Log protection mechanisms (encryption, access controls)

---

### AU.1.002 / NIST 3.3.2 - Enable Auditing
**Control:** Enable audit logging for system components that process CUI.

**Recommended Artifacts:**
- [ ] Audit enablement configuration files
- [ ] System audit policy documentation
- [ ] Logging infrastructure diagram
- [ ] Log source inventory (all CUI-processing systems)
- [ ] Audit control documentation
- [ ] System component classification (CUI vs non-CUI)

---

### AU.1.003 / NIST 3.3.3 - Review Audit Records
**Control:** Review and update audit records.

**Recommended Artifacts:**
- [ ] Audit review schedule and procedures
- [ ] Audit review logs/reports
- [ ] Log analysis reports (automated + manual)
- [ ] Security incident logs correlated with audit data
- [ ] Reviewer training records
- [ ] Escalation procedures for audit anomalies
- [ ] Audit review sign-off sheets

---

### AU.1.004 / NIST 3.3.4 - Alert in Case of Audit Failure
**Control:** Alert in the event of an audit logging process failure.

**Recommended Artifacts:**
- [ ] Audit monitoring/alerting configuration
- [ ] Alert contact list
- [ ] Failure response procedures
- [ ] Alert testing records (proof alerts work)
- [ ] Backup logging mechanism documentation
- [ ] Incident response procedures for audit failures

---

### AU.1.005 / NIST 3.3.5 - Time Synchronization
**Control:** Use internal system clocks to generate time stamps for audit records.

**Recommended Artifacts:**
- [ ] Time synchronization policy (NTP)
- [ ] NTP server configuration documentation
- [ ] Time sync logs
- [ ] Time drift monitoring reports
- [ ] System time settings documentation
- [ ] NTP authentication documentation (if applicable)

---

### AU.1.006 / NIST 3.3.6 - Protect Audit Information
**Control:** Protect audit information and tools from unauthorized access, modification, or deletion.

**Recommended Artifacts:**
- [ ] Audit data access control policy
- [ ] Audit storage encryption documentation
- [ ] Log access logs (who accessed logs)
- [ ] Audit system backup procedures
- [ ] Write-once/WORM storage configuration
- [ ] Privileged access to audit tools list
- [ ] Audit integrity verification procedures

---

## Domain 4: Configuration Management (CM)

### CM.1.001 / NIST 3.4.1 - Baseline Configuration
**Control:** Establish and maintain baseline configurations.

**Recommended Artifacts:**
- [ ] Approved baseline configuration documents
- [ ] Baseline approval signatures
- [ ] Configuration management plan
- [ ] Golden image/repository documentation
- [ ] Baseline version control records
- [ ] Deviation request procedures and logs
- [ ] System configuration inventory

---

### CM.1.002 / NIST 3.4.2 - Track Changes
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

### CM.1.003 / NIST 3.4.3 - Security Impact Analysis
**Control:** Perform security impact analysis prior to making changes.

**Recommended Artifacts:**
- [ ] Security impact analysis methodology
- [ ] Change risk assessment templates
- [ ] Security impact review logs
- [ ] Stakeholder sign-off for changes
- [ ] Pre- and post-change security testing results
- [ ] Vulnerability scan reports pre/post change

---

### CM.1.004 / NIST 3.4.4 - Vulnerability Scanning
**Control:** Scan for vulnerabilities and remediate them.

**Recommended Artifacts:**
- [ ] Vulnerability scanning policy and schedule
- [ ] Scan reports (automated and manual)
- [ ] Vulnerability remediation plans
- [ ] Remediation verification reports
- [ ] Exception approval documentation
- [ ] Scanning tool configuration and updates

---

### CM.1.005 / NIST 3.4.5 - Anti-Malware
**Control:** Employ anti-malware mechanisms.

**Recommended Artifacts:**
- [ ] Anti-malware/EDR deployment records
- [ ] Anti-malware configuration policies
- [ ] Signature/definition update schedules
- [ ] Malware detection logs
- [ ] Malware incident response procedures
- [ ] Exemption documentation (if any systems excluded)

---

### CM.1.006 / NIST 3.4.6 - Incident Response Testing
**Control:** Perform incident response testing.

**Recommended Artifacts:**
- [ ] Incident response plan (IRP)
- [ ] Incident response test schedules
- [ ] Test scenarios and playbooks
- [ ] Test execution reports (after-action reports)
- [ ] Lessons learned documentation
- [ ] IR plan version control and approvals

---

### CM.1.007 / NIST 3.4.7 - Emergency Access
**Control:** Establish alternate means of access.

**Recommended Artifacts:**
- [ ] Emergency access procedures
- [ ] Break-glass account documentation
- [ ] Emergency access approval forms
- [ ] Emergency access logs (when used)
- [ ] Emergency access audit reports
- [ ] Emergency contact lists

---

## Domain 5: Identification and Authentication (IA)

### IA.1.001 / NIST 3.5.1 - Identify and Authenticate Users
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

### IA.1.002 / NIST 3.5.2 - Multi-Factor Authentication
**Control:** Use multi-factor authentication.

**Recommended Artifacts:**
- [ ] MFA policy and scope documentation
- [ ] MFA solution deployment records
- [ ] MFA enforcement configuration
- [ ] Exception approval documentation
- [ ] MFA backup/recovery procedures
- [ ] MFA enrollment/completion reports

---

### IA.1.003 / NIST 3.5.3 - Device Authentication
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

### IA.1.004 / NIST 3.5.4 - Replay Protection
**Control:** Employ replay-resistant authentication mechanisms.

**Recommended Artifacts:**
- [ ] Authentication mechanism documentation
- [ ] Replay attack protection configuration
- [ ] Session management policies
- [ ] Token/session expiration settings
- [ ] Authentication protocol specifications

---

### IA.1.005 / NIST 3.5.5 - Fail-Safe Auth
**Control:** Prevent authentication mechanisms from providing access in fail-safe mode.

**Recommended Artifacts:**
- [ ] Fail-safe authentication documentation
- [ ] Authentication system hardening evidence
- [ ] Backup authentication system configuration
- [ ] Failure mode testing results

---

### IA.1.006 / NIST 3.5.6 - Token Authenticators
**Control:** Accept only PIV-compliant credentials.

**Recommended Artifacts:**
- [ ] PIV card policy
- [ ] PIV card inventory
- [ ] PIV reader deployment records
- [ ] Smart card management procedures
- [ ] PIV exemption documentation (if applicable)
- [ ] CAC/PIV integration documentation

---

### IA.1.007 / NIST 3.5.7 - Cryptographic Modules
**Control:** Employ FIPS-validated cryptography.

**Recommended Artifacts:**
- [ ] FIPS-validated module inventory
- [ ] Cryptographic module certificates (FIPS 140-2/140-3)
- [ ] Encryption policy (algorithms, key lengths)
- [ ] Cryptographic module configuration
- [ ] Key management procedures
- [ ] FIPS compliance review reports
- [ ] NIST SP 800-52 documentation reference

---

## Domain 6: Incident Response (IR)

### IR.1.001 / NIST 3.6.1 - IR Policy and Procedures
**Control:** Establish and maintain incident response policy and procedures.

**Recommended Artifacts:**
- [ ] Incident response policy (signed and approved)
- [ ] Incident response procedures/playbooks
- [ ] Incident classification matrix
- [ ] Reporting procedures documentation
- [ ] Incident response team (IRT) roster
- [ ] Escalation matrix
- [ ] IR plan approval and distribution records

---

### IR.1.002 / NIST 3.6.2 - IR Training
**Control:** Ensure IR personnel are trained.

**Recommended Artifacts:**
- [ ] IR team training records
- [ ] IR training curriculum
- [ ] Certification/training certificates
- [ ] Skill gap analysis documentation
- [ ] Cross-training records

---

### IR.1.003 / NIST 3.6.3 - IR Testing
**Control:** Test IR capabilities.

**Recommended Artifacts:**
- [ ] IR testing schedule
- [ ] Test scenarios and objectives
- [ ] Test execution reports
- [ ] Tabletop exercise documentation
- [ ] After-action reports (AARs)
- [ ] Lessons learned and improvement plans

---

### IR.1.004 / NIST 3.6.4 - Incident Monitoring
**Control:** Track and document incidents.

**Recommended Artifacts:**
- [ ] Incident tracking system logs
- [ ] Incident reports (all incidents)
- [ ] Incident timeline documentation
- [ ] Root cause analysis reports
- [ ] Incident closure documentation
- [ ] Trend analysis reports
- [ ] Notification records (if external reporting required)

---

### IR.1.005 / NIST 3.6.5 - Incident Reporting
**Control:** Ensure incidents are reported.

**Recommended Artifacts:**
- [ ] Incident reporting procedures
- [ ] Reporting channel documentation
- [ ] Awareness campaign materials
- [ ] Anonymous reporting mechanism documentation
- [ ] Reporting acknowledgment receipts
- [ ] Mandatory reporting triggers

---

## Domain 7: Maintenance (MA)

### MA.1.001 / NIST 3.7.1 - Maintenance Policy
**Control:** Establish and maintain maintenance policy and procedures.

**Recommended Artifacts:**
- [ ] Maintenance policy
- [ ] Maintenance procedures documentation
- [ ] Maintenance schedule/calendar
- [ ] Maintenance personnel access documentation
- [ ] Vendor maintenance agreements
- [ ] Change management integration procedures

---

### MA.1.002 / NIST 3.7.2 - Maintenance Tools
**Control:** Ensure maintenance tools are approved and controlled.

**Recommended Artifacts:**
- [ ] Approved maintenance tools inventory
- [ ] Tool approval process documentation
- [ ] Maintenance tool access controls
- [ ] Tool usage logs
- [ ] Remote maintenance access procedures
- [ ] Vendor maintenance personnel agreements

---

### MA.1.003 / NIST 3.7.3 - Maintenance Logs
**Control:** Maintain maintenance logs.

**Recommended Artifacts:**
- [ ] Maintenance log templates
- [ ] Maintenance activity records
- [ ] Log review procedures
- [ ] Scheduled vs. unscheduled maintenance documentation
- [ ] Maintenance completion sign-offs

---

### MA.1.004 / NIST 3.7.4 - Maintenance Personnel
**Control:** Ensure maintenance personnel are supervised.

**Recommended Artifacts:**
- [ ] Maintenance supervision procedures
- [ ] Personnel background check records
- [ ] Non-disclosure agreements (NDAs)
- [ ] Escort/chaperone procedures
- [ ] Maintenance access logs with supervisor signatures

---

## Domain 8: Media Protection (MP)

### MP.1.001 / NIST 3.8.1 - Access to Media
**Control:** Protect CUI on media.

**Recommended Artifacts:**
- [ ] Media access control policy
- [ ] Media inventory (USB drives, external hard drives, etc.)
- [ ] CUI media labeling procedures
- [ ] Media checkout/check-in logs
- [ ] Media destruction procedures
- [ ] Removable media disablement evidence (if applicable)
- [ ] Encrypted media deployment records

---

### MP.1.002 / NIST 3.8.2 - Media Sanitization
**Control:** Sanitize media before reuse or release.

**Recommended Artifacts:**
- [ ] Media sanitization policy (NIST SP 800-88)
- [ ] Sanitization procedures documentation
- [ ] Sanitization method inventory (degauss, wipe, shred)
- [ ] Sanitization logs (before release/reuse)
- [ ] Sanitization equipment certification
- [ ] Disposal documentation and certificates

---

### MP.1.003 / NIST 3.8.3 - Media Transport
**Control:** Control media transport.

**Recommended Artifacts:**
- [ ] Media transport policy
- [ ] Transport chain-of-custody documentation
- [ ] Encrypted transport procedures
- [ ] Approved carrier agreements
- [ ] Transport logs and receipts
- [ ] Transport security procedures (courier, armored, etc.)

---

### MP.1.004 / NIST 3.8.4 - Media Marking
**Control:** Mark media with CUI designation and control markings.

**Recommended Artifacts:**
- [ ] CUI marking policy/procedures
- [ ] Control markings guide (CUI, CUI//SP-SIMP, etc.)
- [ ] Marking compliance audit reports
- [ ] Document templates with CUI markings
- [ ] Training materials on CUI markings

---

## Domain 9: Physical Protection (PE)

### PE.1.001 / NIST 3.9.1 - Physical Access Policy
**Control:** Establish and maintain physical access policy.

**Recommended Artifacts:**
- [ ] Physical security policy
- [ ] Access control zone documentation
- [ ] Badge access procedures
- [ ] Visitor access procedures
- [ ] Physical access logs (entry/exit)
- [ ] Key/cipher lock control documentation
- [ ] Security officer responsibilities

---

### PE.1.002 / NIST 3.9.2 - Access Authorization
**Control:** Ensure physical access to CUI is authorized.

**Recommended Artifacts:**
- [ ] Access authorization matrix
- [ ] Badge issuance procedures
- [ ] Temporary access request forms
- [ ] Access revocation procedures
- [ ] Personnel clearance documentation (if applicable)
- [ ] Escort procedures for visitors

---

### PE.1.003 / NIST 3.9.3 - Visitor Control
**Control:** Monitor and control physical access.

**Recommended Artifacts:**
- [ ] Visitor management procedures
- [ ] Visitor sign-in/out logs
- [ ] Badge expiration schedules
- [ ] Physical security monitoring reports
- [ ] Lost/stolen badge procedures
- [ ] Badge photo/identification documentation

---

### PE.1.004 / NIST 3.9.4 - Physical Access Monitoring
**Control:** Physical access to CUI is monitored.

**Recommended Artifacts:**
- [ ] Physical security camera deployment map
- [ ] Access monitoring procedures
- [ ] Alarm/door sensor configuration
- [ ] Physical intrusion logs
- [ ] Security monitoring shift logs
- [ ] Physical incident reports

---

### PE.1.005 / NIST 3.9.5 - Equipment Maintenance
**Control:** Maintain physical access equipment.

**Recommended Artifacts:**
- [ ] Physical security equipment inventory
- [ ] Equipment maintenance schedule
- [ ] Calibration records (sensors, locks)
- [ ] Equipment testing documentation
- [ ] Replacement/upgrade logs

---

### PE.1.006 / NIST 3.9.6 - Delivery Areas
**Control:** Control physical access to delivery areas.

**Recommended Artifacts:**
- [ ] Delivery area security procedures
- [ ] Receiving area access controls
- [ ] Package inspection procedures
- [ ] Delivery log documentation
- [ ] Courier/vendor access agreements

---

## Domain 10: Risk Assessment (RA)

### RA.1.001 / NIST 3.11.1 - Risk Assessment Policy
**Control:** Establish and maintain risk assessment policy.

**Recommended Artifacts:**
- [ ] Risk management policy
- [ ] Risk assessment methodology
- [ ] Risk tolerance statements
- [ ] Risk assessment schedule
- [ ] Risk register
- [ ] Risk assessment templates

---

### RA.1.002 / NIST 3.11.2 - Scan for Vulnerabilities
**Control:** Scan CUI systems for vulnerabilities.

**Recommended Artifacts:**
- [ ] Vulnerability scanning policy
- [ ] Scan schedule (quarterly/annual)
- [ ] Vulnerability scan reports
- [ ] False positive documentation
- [ ] Scan tool configuration
- [ ] Scan scope documentation

---

### RA.1.003 / NIST 3.11.3 - Remediate Vulnerabilities
**Control:** Remediate vulnerabilities.

**Recommended Artifacts:**
- [ ] Vulnerability remediation plan
- [ ] Patch management policy
- [ ] Patch deployment schedules
- [ ] Remediation verification reports
- [ ] Exception approval documentation
- [ ] Risk acceptance documentation

---

### RA.1.004 / NIST 3.11.4 - Update Risk Assessments
**Control:** Update risk assessments periodically.

**Recommended Artifacts:**
- [ ] Risk assessment update schedule
- [ ] Current risk assessment report
- [ ] Risk review meeting minutes
- [ ] Risk trend analysis
- [ ] Risk acceptance sign-offs
- [ ] Risk committee documentation

---

## Domain 11: Security Assessment (CA)

### CA.1.001 / NIST 3.12.1 - Security Assessment Policy
**Control:** Establish and maintain security assessment policy.

**Recommended Artifacts:**
- [ ] Security assessment policy
- [ ] Assessment schedule
- [ ] Assessment team credentials
- [ ] Assessment methodology documentation
- [ ] Third-party assessor agreements (if applicable)
- [ ] Assessment scope documentation

---

### CA.1.002 / NIST 3.12.2 - Assess Security Controls
**Control:** Assess security controls.

**Recommended Artifacts:**
- [ ] Security control assessment reports
- [ ] Control effectiveness testing results
- [ ] Penetration testing reports
- [ ] Independent assessment documentation
- [ ] Control gap analysis
- [ ] Control testing procedures

---

### CA.1.003 / NIST 3.12.3 - Remediation Plan
**Control:** Develop and implement remediation plans.

**Recommended Artifacts:**
- [ ] Plan of Action and Milestones (POAM)
- [ ] Gap remediation schedules
- [ ] Remediation responsibility assignments
- [ ] POAM tracking logs
- [ ] Remediation completion evidence
- [ ] POAM status reports

---

### CA.1.004 / NIST 3.12.4 - System Security Plan
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

### CA.1.005 / NIST 3.12.5 - Update SSP
**Control:** Update SSP to reflect changes.

**Recommended Artifacts:**
- [ ] SSP update procedures
- [ ] SSP change logs
- [ ] SSP version control
- [ ] Update approval documentation
- [ ] SSP review and sign-off records
- [ ] SSP distribution notifications

---

### CA.1.006 / NIST 3.12.6 - External Connections Review
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

### CA.1.007 / NIST 3.12.7 - Continuous Monitoring
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

### CA.1.008 / NIST 3.12.8 - Security Assessments on Change
**Control:** Perform security assessments on changes.

**Recommended Artifacts:**
- [ ] Pre-change security test procedures
- [ ] Post-change security test results
- [ ] Change security impact assessments
- [ ] Regression testing documentation
- [ ] Security testing integration with change management
- [ ] Test environment documentation

---

## Domain 12: System and Communications Protection (SC)

### SC.1.001 / NIST 3.13.1 - Boundary Protection
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

### SC.1.002 / NIST 3.13.2 - Information in Transit
**Control:** Protect information in transit.

**Recommended Artifacts:**
- [ ] Encryption-in-transit policy (TLS 1.2+)
- [ ] TLS/SSL configuration documentation
- [ ] Certificate inventory and expiry tracking
- [ ] VPN encryption documentation
- [ ] Secure transmission protocol documentation
- [ ] FIPS-validated cryptographic module certificates
- [ ] Encryption strength verification reports

---

### SC.1.003 / NIST 3.13.3 - Information at Rest
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

### SC.1.004 / NIST 3.13.4 - CUI Partitioning
**Control:** Separate CUI from non-CUI.

**Recommended Artifacts:**
- [ ] Data partitioning procedures
- [ ] Network segmentation documentation
- [ ] CUI storage location inventory
- [ ] Cross-boundary data flow controls
- [ ] Access control matrix by data classification
- [ ] CUI labeling procedures

---

### SC.1.005 / NIST 3.13.5 - Denial of Service Protection
**Control:** Employ denial-of-service protection.

**Recommended Artifacts:**
- [ ] DoS/DDoS protection policy
- [ ] DoS mitigation tool configuration
- [ ] Bandwidth monitoring reports
- [ ] DoS response procedures
- [ ] ISP/CDN DDoS protection agreements
- [ ] DoS incident logs

---

### SC.1.006 / NIST 3.13.6 - Mobile Code Protection
**Control:** Protect against or limit effects of mobile code.

**Recommended Artifacts:**
- [ ] Mobile code policy (Java, ActiveX, etc.)
- [ ] Browser hardening procedures
- [ ] Application allowlist/denylist
- [ ] Code signing verification procedures
- [ ] Sandboxing/isolation documentation
- [ ] Mobile code blocking logs

---

### SC.1.007 / NIST 3.13.7 - Cryptography Protection
**Control:** Employ cryptography to protect CUI.

**Recommended Artifacts:**
- [ ] Cryptographic standards policy
- [ ] Approved algorithms list (NIST SP 800-52)
- [ ] Encryption strength documentation (key lengths)
- [ ] Key lifecycle management procedures
- [ ] FIPS-validated module inventory
- [ ] Encryption deployment inventory
- [ ] Cryptographic module certificates

---

### SC.1.008 / NIST 3.13.8 - Confidentiality Protection
**Control:** Employ cryptography to protect confidentiality of CUI.

**Recommended Artifacts:**
- [ ] Confidentiality protection policy
- [ ] End-to-end encryption documentation
- [ ] PGP/S/MIME key management
- [ ] Secure email gateway configuration
- [ ] File encryption procedures
- [ ] Secure file transfer protocols (SFTP, etc.)

---

## Domain 13: System and Information Integrity (SI)

### SI.1.001 / NIST 3.14.1 - Flaw Remediation
**Control:** Identify, report, and correct system flaws.

**Recommended Artifacts:**
- [ ] Vulnerability management policy
- [ ] Patch management procedures
- [ ] Vulnerability identification logs
- [ ] Patch deployment schedules
- [ ] Flaw remediation tracking
- [ ] Root cause analysis documentation
- [ ] Patch testing procedures

---

### SI.1.002 / NIST 3.14.2 - Security Software Updates
**Condition:** Update malicious code protection mechanisms.

**Recommended Artifacts:**
- [ ] Anti-malware/EDR update policy
- [ ] Signature update automation configuration
- [ ] Update frequency documentation
- [ ] Update failure notification procedures
- [ ] Anti-malware version inventory
- [ ] Update verification logs

---

### SI.1.003 / NIST 3.14.3 - Security Baseline Updates
**Condition:** Update security baselines.

**Recommended Artifacts:**
- [ ] Security baseline update schedule
- [ ] Baseline version control
- [ ] Baseline approval documentation
- [ ] Update notification procedures
- [ ] Baseline deployment records
- [ ] Configuration drift monitoring reports

---

### SI.1.004 / NIST 3.14.4 - Security Alerts
**Condition:** Monitor system alerts.

**Recommended Artifacts:**
- [ ] Security alert monitoring procedures
- [ ] Alert correlation rules
- [ ] Alert threshold configuration
- [ ] Alert response playbooks
- [ ] SIEM/SOC tool configuration
- [ ] Alert analysis reports
- [ ] False positive documentation

---

### SI.1.005 / NIST 3.14.5 - Software Flaw Scans
**Condition:** Scan for software flaws.

**Recommended Artifacts:**
- [ ] Software scanning policy (SAST/DAST)
- [ ] Static/dynamic analysis scan reports
- [ ] Code review procedures
- [ ] Third-party vulnerability scans
- [ ] Scan frequency documentation
- [ ] Remediation tracking for software flaws

---

### SI.1.006 / NIST 3.14.6 - Timely Remediation
**Condition:** Remediate vulnerabilities in timely manner.

**Recommended Artifacts:**
- [ ] Remediation SLA documentation
- [ ] Vulnerability priority matrix
- [ ] Remediation tracking system logs
- [ ] Overdue vulnerability reports
- [ ] Risk acceptance documentation
- [ ] Remediation delay justifications

---

### SI.1.007 / NIST 3.14.7 - Unauthorized Software
**Condition:** Prohibit unauthorized software.

**Recommended Artifacts:**
- [ ] Software authorization policy
- [ ] Approved software catalog
- [ ] Software deployment procedures
- [ ] Application allowlist configuration
- [ ] Unauthorized software detection logs
- [ ] Software audit reports
- [ ] Shadow IT investigation procedures

---

### SI.1.008 / NIST 3.14.8 - Security Functionality Verification
**Condition:** Verify security functionality.

**Recommended Artifacts:**
- [ ] Security control testing schedule
- [ ] Functionality test reports
- [ ] Control effectiveness validation
- [ ] Security testing methodologies
- [ ] Test environment documentation
- [ ] Third-party validation reports (if applicable)

---

## Domain 14: System and Communications Protection (SC) - continued

### SC.1.009 / NIST 3.13.9 - Session Protection
**Control:** Terminate sessions after inactivity.

**Recommended Artifacts:**
- [ ] Session timeout policy
- [ ] Timeout configuration documentation
- [ ] Application timeout settings evidence
- [ ] Session lock enforcement logs
- [ ] Idle session monitoring reports

---

### SC.1.010 / NIST 3.13.10 - Wireless Access
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

## Domain 15: Personnel Security (PS)

### PS.1.001 / NIST 3.15.1 - Personnel Screening
**Control:** Screen personnel prior to authorization.

**Recommended Artifacts:**
- [ ] Personnel screening policy
- [ ] Background check procedures
- [ ] Screening documentation for authorized personnel
- [ ] Security clearance documentation (if applicable)
- [ ] Screening exemption procedures
- [ ] Screening vendor agreements

---

### PS.1.002 / NIST 3.15.2 - Termination Procedures
**Control:** Ensure personnel exit procedures.

**Recommended Artifacts:**
- [ ] Offboarding procedures checklist
- [ ] Access revocation logs (accounts, badges, keys)
- [ ] Equipment return documentation
- [ ] Exit interview records
- [ ] NDA reminders/acknowledgments
- [ ] Post-termination access review

---

## Priority Artifact Checklist (By Document Type)

### **Must-Have (Priority 1)**
- [ ] System Security Plan (SSP)
- [ ] Plan of Action and Milestones (POAM)
- [ ] Security policies for all domains
- [ ] Incident Response Plan (IRP)
- [ ] Risk Management Policy
- [ ] Access Control Policy
- [ ] Configuration Management Policy

### **Highly Recommended (Priority 2)**
- [ ] Change control procedures and logs
- [ ] Vulnerability scan reports
- [ ] Audit review documentation
- [ ] Training records (all personnel)
- [ ] Physical security procedures
- [ ] Maintenance procedures and logs
- [ ] External connection inventory

### **Best Practice (Priority 3)**
- [ ] Detailed user access matrices
- [ ] Separation of duties matrix
- [ ] Baseline configurations
- [ ] Encryption certificates (FIPS validation)
- [ ] Testing and assessment reports
- [ ] Continuous monitoring documentation

---

## Evidence Organization Tips

### **Folder Structure Suggestion:**
```
CMMC_Evidence/
├── 01_Access_Control/
├── 02_Awareness_Training/
├── 03_Audit_Accountability/
├── 04_Configuration_Management/
├── 05_Identification_Authentication/
├── 06_Incident_Response/
├── 07_Maintenance/
├── 08_Media_Protection/
├── 09_Physical_Protection/
├── 10_Risk_Assessment/
├── 11_Security_Assessment/
├── 12_System_Comms_Protection/
├── 13_System_Info_Integrity/
├── 14_Personnel_Security/
├── SSP_and_Policies/
└── POAM/
```

### **Evidence Lifecycle:**
1. **Create** — Following artifact naming convention
2. **Validate** — Ensure evidence meets control requirement
3. **Store** — Secure location with proper access controls
4. **Version** — Track updates with date stamps
5. **Review** — Annual review for currency
6. **Archive** — Retain per record retention policy

---

## Common Evidence Types by Control Category

| Category | Common Evidence Types |
|----------|---------------------|
| **Policies** | Signed policy documents, acknowledgments |
| **Procedures** | SOPs, runbooks, workflow documentation |
| **Technical Config** | Screenshots, config files, settings exports |
| **Logs** | Audit logs, access logs, system event logs |
| **Reviews** | Review checklists, sign-off sheets, meeting minutes |
| **Training** | Completion records, certificates, test scores |
| **Testing** | Test reports, scan results, after-action reports |
| **Inventories** | System/device inventories, software lists |
| **Diagrams** | Network diagrams, data flow diagrams, architecture |
| **Agreements** | Contracts, MOUs, SLAs, vendor agreements |

---

**Last Updated:** 2026-03-31
**Source:** Steris_Mar_2026_DCG_CMMC_Tracking_v19.xlsx analysis
**Version:** 1.0

---

_Note: This artifact guide provides general recommendations for NIST 800-171/CMMC compliance. Always reference the official NIST 800-171A Assessment Objectives and your organization's specific implementation requirements for definitive guidance._
