Feature: vAPP run command

    Scenario: run command
      """
      correct user name and wrong password entered. Login is unsuccesful
      """
      Given vapp login page opened

      When login using set of specific user and password
        |username          | password     | action    |
        | seconfig         | remember     | LoginSuccess|
      And click download command on sidemenu
      Then click export logs link