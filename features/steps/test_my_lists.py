

@when('I create a list with first item "{first_item_text}"')
def create_a_list(context, first_item_text):
    context.browser.get(context.server_url)
    context.browser.find_element_by_id('id_text').send_keys(first_item_text)
    context.browser.find_element_by_id('id_text').send_keys('\n')

@when('I add an item "{item_text}"')
def add_an_item(context, item_text):
    context.browser.find_element_by_id('id_text').send_keys(item_text)
    context.browser.find_element_by_id('id_text').send_keys('\n')

@then('I will see a link to "{link_text}"')
def see_a_link(context, link_text):
    context.browser.find_element_by_link_text(link_text)

@when('I click the link to "{link_text}"')
def click_link(context, link_text):
    context.browser.find_element_by_link_text(link_text).click()

@then('I will be on the "{first_item_text}" list page')
def step_impl(context, first_item_text):
    table = context.browser.find_element_by_id('id_list_table')
    rows = table.find_elements_by_tag_name('tr')
    expected_row_text = '1: ' + first_item_text
    assert rows[0].text == expected_row_text