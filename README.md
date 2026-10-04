# Campus LAN Automation Suite

An enterprise network automation framework designed to streamline device reachability audits, multi-threaded connectivity validation, and dynamic templated provisioning across an emulated Cisco IOS campus network in PNETLab.

---

## 📅 Architecture Roadmap & Implementation Status

| Milestone | Capability / Feature | Status | Demo Link |
| :--- | :--- | :---: | :--- |
| **Milestone 1** | Campus collapsed-core topology, L3 routing gateway, & dedicated management VLAN 99 | ✅ Complete | [View Topology](#-milestone-1-topology--in-band-management) |
| **Milestone 2** | Multi-threaded SSH reachability audit & defensive fault isolation | ✅ Complete | [Watch Demos](#-milestone-2-ssh-reachability--fault-tolerance) |
| **Milestone 3** | Automated VLAN provisioning engine (Jinja2 templates + YAML data models) | 🔄 In Progress | Coming Soon |


---

## 🏗️ Milestone 1: Topology & Management Architecture

Designed a collapsed core/distribution architecture with segmented management isolation on **VLAN 99**:

![Milestone 1 Topology](/demos/topology.png)

* **`L3-core` (`10.99.0.1`):** Serves as the Inter-VLAN default gateway, interconnected with external management via `Cloud0`.
* **`ASW1`–`ASW4` (`10.99.0.10`–`40`):** Managed remotely via isolated Layer 2 SVIs (`interface Vlan 99`).

---

## ⚡ Milestone 2: SSH Reachability & Fault Tolerance

Automated fleet connectivity pre-check utility utilizing **Netmiko** and **concurrent.futures** to validate infrastructure state prior to executing configuration pushes:

* **Concurrent Discovery:** Validates SSH reachability across all operational switches in parallel, avoiding blocking execution delays.
* **Socket Timeout Handling:** Gracefully isolates offline nodes (demonstrated with powered-off `ASW2`) via `NetmikoTimeoutException` handling without terminating the audit cycle.
* **Authentication Trap:** Captures invalid credential attempts cleanly via `NetmikoAuthenticationException`.


### Execution Verifications

#### 1. Baseline Fleet Reachability (All Nodes Active)
![Baseline Reachability](/demos/reachability_baseline_success.gif)

#### 2. Fault Isolation: Unreachable Node / Connection Timeout
![Timeout Handling](/demos/reachability_timeout_handling.gif)

#### 3. Fault Isolation: Authentication Rejection
![Auth Failure Handling](/demos/reachability_auth_failure.gif)

---

## 🛠️ Tech Stack & Prerequisites

* **Emulation:** PNETLab, Cisco IOL / vIOS-L2
* **Scripting & Concurrency:** Python 3, `concurrent.futures`, `netmiko`
