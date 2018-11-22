Ansible role: "Red Hat Single Sign-On"
=================================


Description
-----------

Advanced Ansible role that manages [Red Hat Single Sign-On](https://access.redhat.com/products/red-hat-single-sign-on) instances.

Core implemented features in this role:

- multiple parallel versions and profile support
- multiple Red Hat JBoss EAP instances per host
- graceful orchestration and shutdown (prerequisite for rolling updates)
- configuration of the Red Hat JBoss EAP instances using the CLI
- infinispan fine tuning
- cleanup after installation

This role is based on:

- https://github.com/Maarc/ansible_middleware_soe showing how to easily operate Red Hat JBoss middleware products using ansible role.
- https://github.com/Maarc/ansible-role-redhat-jboss-eap
- https://github.com/Maarc/ansible-role-redhat-jboss-common

Requirements
------------

This role has been tested on Ansible 2.0.2.0 and 2.1.1.0. It requires Red Hat Enterprise Linux 7.


Dependencies
------------

### TODO: Remove this dependency
The "Maarc.rh-jboss-common" role is required. It could be imported as follows:

    ansible-galaxy install Maarc.rh-jboss-common -p roles

or

    ansible-galaxy install -r requirements.yml -p roles


Installation
------------

### TODO


Role Variables
--------------

### TODO
*General variables*

| Name              | Default Value       | Description          |
|-------------------|---------------------|----------------------|
| `download_dir` | `/tmp` | Directory containing all required middleware binaries on the managed remote host. Mandatory |
| `jboss.user` | `jboss` | Linux user name used for running EAP |
| `jboss.group` | `jboss` | Linux group name used for the `jboss.user` |
| `jboss.group_id` | `500` | Linux group id taken for `jboss.group` |
| `jboss.user_home` | `/opt/jboss` | Linux home directory for `jboss.user`  |


*Instance specific variables*

| Name              | Default Value       | Description          |
|-------------------|---------------------|----------------------|
| `jboss_eap_instance_name` | `default` | Name of the separate running Red Hat JBoss EAP instance. Mandatory |
| `jboss_eap_instance_admin_user` | `redhat` | Red Hat JBoss EAP admin user name. Mandatory |
| `jboss_eap_instance_admin_password` | `ba2caa9378fa898f1dea88804abe52b4` | Red Hat JBoss EAP admin password ("redhat123!") hashed according to HEX( MD5( username ':' realm ':' password)). Mandatory |
| `jboss_eap_instance_admin_groups` | empty | Red Hat JBoss EAP admin user groups |
| `jboss_eap_golden_image_name` | empty | Name of the used Red Hat JBoss EAP golden image. Mandatory |
| `jvm_xm` | `512` | Value for the xms and xmx (both are set equal) in MB  |
| `jboss_eap_instance_port_offset` | `0` | Port offset for the JBoss EAP instance  |
| `jboss_eap_instance_cli_used_default_port` | `9999` | Default port for the native management interface |
| `jboss_eap_instance_cli_default_port` | `8888` | Port used only during updates using the CLI (port should be available) |
| `jboss_eap_instance_standalone_file` | `standalone.xml` | Name of the used standalone XML file |


*Usage of CLI files for the JBoss EAP configuration*

| Name              | Default Value       | Description          |
|-------------------|---------------------|----------------------|
| `cli_list` | `{ }` | List of CLI files to be used for the configuration |
| `cli_dir` | empty | Local directory containing the CLI files in cli_list. Mandatory if `cli_list` is not empty |


Example Playbook
----------------

### TODO
Here is a playbook creating three JBoss EAP instances on every host in "jboss-group":

    - hosts: "jboss-group"
      roles:
        # JBoss EAP 7 instance for the ticket-monster application
        - {
            role: "Maarc.rh-jboss-eap",
            jboss_eap_golden_image_name: "jboss-eap-6.4.8_GI",
            jboss_eap_instance_name: "ticket_monster",
            jboss_eap_instance_standalone_file: "standalone-full-ha.xml",
            jboss_eap_instance_port_offset: 0,
            app_list: { "ticket-monster.war" },
            cli_list: { "add_datasource.cli", "add_mod_cluster_6.cli"},
        }
        # JBoss EAP 7 instance for the petclinic application
        - {
            role: "Maarc.rh-jboss-eap",
            jboss_eap_golden_image_name: "jboss-eap-7.0.1_GI",
            jboss_eap_instance_name: "petclinic",
            jboss_eap_instance_standalone_file: "standalone-full-ha.xml",
            jboss_eap_instance_port_offset: "1000",
            app_mvn_list: [ { g: "com.redhat.jboss", a: "petclinic.war", v: "1.0", e: "war" } ],
            cli_list: { "add_datasource.cli", "add_mod_cluster_7.cli"}
        }
        # JBoss EAP 7 instance for the jenkins application
        - {
            role: "Maarc.rh-jboss-eap",
            jboss_eap_golden_image_name: "jboss-eap-7.0.1_GI",
            jboss_eap_instance_name: "jenkins",
            jboss_eap_instance_standalone_file: "standalone-full-ha.xml",
            jboss_eap_instance_port_offset: 2000,
            app_list: { "jenkins.war" },
            cli_list: { "add_datasource.cli", "add_mod_cluster_7.cli"},
        }


Structure
---------

### TODO

- `defaults/main.yml` centralize the default variables that could be overridden
- `tasks/main.yml` coordinate the execution of the different tasks
- `tasks/00__prepare.yml` check and create the linux user, group and home directory for the JBoss instance.
- `tasks/01__copy_and_unpack.yml` download the selected golden image in the `download_dir` and unzip it
- `tasks/02__configure.yml` used to check potential changes to the existing configuration (step 02) and to conduct the changes if necessary (step 04)
- `tasks/03__graceful_removal.yml` gracefully stops and removes the current running instance if necessary (based on the outcome of step 02)
- `tasks/05__register_service.yml` register the instance as a linux service
- `vars/main.yml` centralize some convenience variables that should not be overridden


License
-------

[Apache 2.0](./LICENSE)


Author Information
------------------

* [Raphael Abreu](https://github.com/aelkz)
* [Marcelo Ataxexe](https://github.com/ataxexe)