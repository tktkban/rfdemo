*** Settings ***
Library    OperatingSystem
Library    NetmikoOperator.py

*** Test Cases ***
Login to router
    OPEN SESSION    ${IP}    ${user}    ${pass}    cisco_xr    ${hostname}

Check if state : Initial check
    ${return}=    CHECK IF STATE    ${ifname}    ${hostname}
    Should Be True    ${return}

Shutdown Interface
    SHUTDOWN INTERFACE    ${ifname}    shutdown-interface    ${hostname}

Check if state : after shutdown
    ${return}=    CHECK IF STATE    ${ifname}    ${hostname}
    Should Not Be True    ${return}

No Shutdown Interface
    NOSHUTDOWN INTERFACE    ${ifname}    shutdown-interface    ${hostname}

Check if state : after no shutdown
    ${return}=    CHECK IF STATE    ${ifname}    ${hostname}
    Should Be True    ${return}

Logout from router
    CLOSE SESSION    ${hostname}