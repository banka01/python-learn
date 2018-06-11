

Feature: vAPP Force Change Password

    Scenario: Authentication failure with correct username and wrong password
      """
      correct user name and wrong password entered. Login is unsuccesful
      """
      Given vapp login page opened

      When login using set of specific user and password
        |username          | password     | action    |
        | seconfig         | seconf       | LoginError|

      Then Authentication failure


    Scenario: Authentication Success and password reset with valid and invalid password
      Given vapp login page opened

      When login using set of specific user and password
        |username          | password       | action              |
        | seconfig         | seconfig       | password_reset_page |

      Then Password reset page displayed
      And enter new password and confirm password
        |newpassword       | confirmpassword| action            |
        | seconfig         | remembeer123   | failure_mismatch  |
        | seconfig         |                | failure_empty     |
        | secon            | secon          | failure_size      |
        | remember         | remember       | success           |



