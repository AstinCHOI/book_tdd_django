from selenium import webdriver
from .base import FunctionalTest


def quit_if_possible(browser):
    try: browser.quit()
    except: pass


class SharingTest(FunctionalTest):

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        self.create_pre_authenticated_session('astinchoi@mockmyid.com')
        astin_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(astin_browser))

        oni_browser = webdriver.Firefox()
        self.addCleanup(lambda: quit_if_possible('oniciferous@example.com'))
        self.create_pre_authenticated_session('oniciferous@example.com')

        self.browser = astin_browser
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('Get help\n')

        share_box = self.browser.find_element_by_css_selector('input[name=email]')
        self.assertEqual(
            share_box.get_attribute('placeholder'),
            'your-friend@example.com'
        )