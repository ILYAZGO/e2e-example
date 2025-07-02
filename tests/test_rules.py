#from playwright.sync_api import Page, expect
from utils.variables import *
from pages.rules import *
from utils.create_delete_user import create_user, delete_user, give_users_to_manager
import pytest
import allure

@pytest.mark.e2e
@pytest.mark.rules
@allure.title("test_add_rule_inside_group")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("Create rule inside group by user")
def test_add_rule_inside_group(base_url, page: Page) -> None:
    rules = Rules(page)

    with allure.step("Create user"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_USER, PASSWORD)

    with allure.step("Go to url"):
        rules.navigate(base_url)

    with allure.step("Auth with user"):
        rules.auth(LOGIN, PASSWORD)

    with allure.step("Go to markup"):
        rules.click_markup()

    with allure.step("Press (Create group)"):
        rules.press_create_group()

    with allure.step("Check that (Add) button disabled"):
        expect(rules.button_accept).to_be_disabled()

    with allure.step("Add group name"):
        rules.input_new_group_name("99999")

    with allure.step("Wait and check snack bar"):
        rules.check_alert("Группа добавлена")

    with allure.step("Click at new group"):
        page.locator(GROUP_LIST).get_by_text("99999").click()
        page.wait_for_selector('[aria-label="Чтобы добвить тег, выберите или добавьте группу."]', state='hidden')

    with allure.step("Press (Create rule)"):
        rules.press_create_rule()

    with allure.step("Check that (Add) button disabled"):
        expect(rules.button_accept).to_be_disabled()

    with allure.step("Add rule name"):
        rules.input_new_rule_name("88888")

    with allure.step("Wait and check snack bar"):
        rules.check_alert("Тег добавлен")

    with allure.step("Check that rule and group created"):
        page.wait_for_selector(INPUT_TAG_RULE_NAME)
        expect(rules.input_tag_rule_name).to_have_value("88888", timeout=wait_until_visible) #check rule

    with allure.step("Delete rule"):
        rules.delete_rule_or_dict()

    with allure.step("Wait and check snack bar"):
        rules.check_alert("Правило удалено")

    with allure.step("Delete group"):
        rules.delete_group()

    with allure.step("Wait and check snack bar"):
        rules.check_alert("Группа удалена")

    with allure.step("Check that deleted"):
        expect(page.get_by_text("99999")).not_to_be_visible(timeout=wait_until_visible) #check no parent group

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN, USER_ID)


@pytest.mark.e2e
@pytest.mark.rules
@allure.title("test_add_group_of_rules_edit_name_delete")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("Create, rename and delete group of rules")
def test_add_group_of_rules_edit_name_delete(base_url, page: Page) -> None:
    rules = Rules(page)

    with allure.step("Create user"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_USER, PASSWORD)

    with allure.step("Go to url"):
        rules.navigate(base_url)

    with allure.step("Auth with user"):
        rules.auth(LOGIN, PASSWORD)

    with allure.step("Go to markup"):
        rules.click_markup()

    #
    with allure.step("Press (Add group) button"):
        rules.press_create_group()

    with allure.step("Press (Cancel) button"):
        page.locator(BUTTON_OTMENA).click()

    with allure.step("Check cancelled"):
        expect(page.locator('[aria-label="Вкл/Выкл"]')).to_have_count(2, timeout=wait_until_visible)
        #expect(page.locator(NI4EGO_NE_NAYDENO)).to_be_visible(timeout=wait_until_visible)  # надпись Ничего не найдено

    with allure.step("Press (Add group) button"):
        rules.press_create_group()

    with allure.step("Press (X) button"):
        rules.close_modal_window()

    with allure.step("Check cancelled"):
        expect(page.locator('[aria-label="Вкл/Выкл"]')).to_have_count(2, timeout=wait_until_visible)
        #expect(page.locator(NI4EGO_NE_NAYDENO)).to_be_visible(timeout=wait_until_visible)  # надпись Ничего не найдено

    with allure.step("Press (Create group)"):
        rules.press_create_group()

    with allure.step("Check that (Add) button disabled"):
        expect(rules.button_accept).to_be_disabled()

    with allure.step("Add rule name"):
        rules.input_new_group_name("12345")

    with allure.step("Wait and check snack bar"):
        rules.check_alert("Группа добавлена")

    with allure.step("Click at new group"):
        page.locator(GROUP_LIST).get_by_text("12345").click()
        page.wait_for_selector('[aria-label="Чтобы добвить тег, выберите или добавьте группу."]', state='hidden')

    with allure.step("Rename group"):
        page.wait_for_selector(BUTTON_PENCIL)
        page.locator(ACTIVE_GROUP).locator(BUTTON_PENCIL).click()
        page.locator(INPUT_EDIT_GROUP_NAME).type("54321", delay=5)
        page.locator(ACTIVE_GROUP).locator(BUTTON_SAVE_EDITED_NAME).get_by_role("button").first.click()

    with allure.step("Wait and check snack bar"):
        rules.check_alert("Название группы изменено")

    with allure.step("Check group created and have edited name"):
        expect(page.get_by_text("54321")).to_be_visible(timeout=wait_until_visible)

    with allure.step("Delete group"):
        rules.delete_group()

    with allure.step("Wait and check snack bar"):
        rules.check_alert("Группа удалена")

    with allure.step("Check group deleted"):
        expect(page.locator(GROUP_LIST).get_by_text("54321")).not_to_be_visible(timeout=wait_until_visible)

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN, USER_ID)


@pytest.mark.e2e
@pytest.mark.rules
@allure.title("test_add_rule_outside_group_disabled")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("Creating rule outside group should be disabled")
def test_add_rule_outside_group_disabled(base_url, page: Page) -> None:
    rules = Rules(page)

    with allure.step("Create user"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_USER, PASSWORD)

    with allure.step("Go to url"):
        rules.navigate(base_url)

    with allure.step("Auth with user"):
        rules.auth(LOGIN, PASSWORD)

    with allure.step("Go to markup"):
        rules.click_markup()

    with allure.step("Check that creating rule - disabled and alert exists"):
        expect(page.locator('[aria-label="Чтобы добавить тег, выберите или добавьте группу."]')).to_have_count(1)

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN, USER_ID)


@pytest.mark.e2e
@pytest.mark.rules
@allure.title("test_add_group_and_rule_with_same_name")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("test_add_group_and_rule_with_same_name. You cant do group and rule with same name (409 status code)")
def test_add_group_and_rule_with_same_name(base_url, page: Page) -> None:
    rules = Rules(page)

    with allure.step("Create user"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_USER, PASSWORD)

    with allure.step("Go to url"):
        rules.navigate(base_url)

    with allure.step("Auth with user"):
        rules.auth(LOGIN, PASSWORD)

    with allure.step("Go to markup"):
        rules.click_markup()

    with allure.step("Press (Create group)"):
        rules.press_create_group()

    with allure.step("Check that (Add) button disabled"):
        expect(rules.button_accept).to_be_disabled()

    with allure.step("Add rule name"):
        rules.input_new_group_name("auto_rule_group")

    with allure.step("Wait and check snack bar"):
        rules.check_alert("Такая группа уже существует")

    with allure.step("Click at existed group"):
        page.locator(GROUP_LIST).get_by_text("auto_rule_group").click()
        page.wait_for_selector('[aria-label="Чтобы добвить тег, выберите или добавьте группу."]', state='hidden')

    with allure.step("Press (Create rule)"):
        rules.press_create_rule()

    with allure.step("Check that (Add) button disabled"):
        expect(rules.button_accept).to_be_disabled()

    with allure.step("Try to create rule with same name"):
        rules.input_new_rule_name("auto_rule")

    with allure.step("Wait and check snack bar"):
        rules.check_alert("Такой тег уже существует")

    with allure.step("Reload page"):
        rules.reload_page()

    with allure.step("Check that tag with same name was not created"):
        expect(page.get_by_text("auto_rule_group", exact=True)).to_have_count(1, timeout=wait_until_visible)
        expect(page.get_by_text("auto_rule", exact=True)).to_have_count(1, timeout=wait_until_visible)

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN, USER_ID)


@pytest.mark.e2e
@pytest.mark.rules
@allure.title("test_check_old_rule")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("DEV-1784   check old rule from Ecotelecom")
def test_check_old_rule(base_url, page: Page) -> None:
    rules = Rules(page)

    with allure.step("Go to url"):
        rules.navigate(base_url)

    with allure.step("Auth with Ecotelecom"):
        rules.auth(ECOTELECOM, ECOPASS)

    with allure.step("Go to markup"):
        rules.click_markup()

    with allure.step("Click at first group"):
        page.wait_for_selector('[href*="/dictionaries?group"]')
        page.locator('[data-testid="test"]').first.click()

    with allure.step("Check that rule opened"):
        page.wait_for_selector(INPUT_TAG_RULE_NAME)
        expect(page.locator('[data-testid="fragmentRuleWhoSaid"]')).to_be_visible(timeout=wait_until_visible)


@pytest.mark.e2e
@pytest.mark.rules
@allure.title("test_add_rule_inside_group_check_fragment_rule")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("Create rule inside group, check rule for fragments")
def test_add_rule_inside_group_check_fragment_rule(base_url, page: Page) -> None:
    rules = Rules(page)

    with allure.step("Create user"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_USER, PASSWORD)

    with allure.step("Go to url"):
        rules.navigate(base_url)

    with allure.step("Auth with user"):
        rules.auth(LOGIN, PASSWORD)

    with allure.step("Go to markup"):
        rules.click_markup()

    with allure.step("Press (Create group)"):
        rules.press_create_group()

    with allure.step("Check that (Add) button disabled"):
        expect(rules.button_accept).to_be_disabled()

    with allure.step("Add rule name"):
        rules.input_new_group_name("99999")

    with allure.step("Wait and check snack bar"):
        rules.check_alert("Группа добавлена")

    with allure.step("Click at group"):
        page.locator(GROUP_LIST).get_by_text("99999").click()
        page.wait_for_selector('[aria-label="Чтобы добвить тег, выберите или добавьте группу."]', state='hidden')

    with allure.step("Press (Create rule)"):
        rules.press_create_rule()

    with allure.step("Check that (Add) button disabled"):
        expect(rules.button_accept).to_be_disabled()

    with allure.step("Add rule name"):
        rules.input_new_rule_name("88888")

    with allure.step("Wait and check snack bar"):
        rules.check_alert("Тег добавлен")

    with allure.step("Check that group created"):
        page.wait_for_selector(INPUT_TAG_RULE_NAME)
        expect(rules.input_tag_rule_name).to_have_value("88888", timeout=wait_until_visible) #check rule

    with allure.step("Add fragment"):
        page.locator('[data-testid="fragmentRuleaddFragment"]').click()

    # switch "who said?"
    with allure.step("Switch (who said?) from first to last"):
        page.locator('[data-testid="fragmentRuleWhoSaid"]').get_by_text("Любой сказал").click()
        page.locator('[data-testid="fragmentRuleWhoSaid"]').get_by_text("Клиент сказал").click()
        page.locator('[data-testid="fragmentRuleWhoSaid"]').get_by_text("Клиент сказал", exact=True).click()
        page.locator('[data-testid="fragmentRuleWhoSaid"]').get_by_text("Сотрудник сказал").click()
        page.locator('[data-testid="fragmentRuleWhoSaid"]').get_by_text("Сотрудник сказал", exact=True).click()
        page.locator('[data-testid="fragmentRuleWhoSaid"]').get_by_text("Любой не сказал").click()
        page.locator('[data-testid="fragmentRuleWhoSaid"]').get_by_text("Любой не сказал", exact=True).click()
        page.locator('[data-testid="fragmentRuleWhoSaid"]').get_by_text("Клиент не сказал").click()
        page.locator('[data-testid="fragmentRuleWhoSaid"]').get_by_text("Клиент не сказал", exact=True).click()
        page.locator('[data-testid="fragmentRuleWhoSaid"]').get_by_text("Сотрудник не сказал").click()
        page.locator('[data-testid="fragmentRuleWhoSaid"]').get_by_text("Сотрудник не сказал", exact=True).click()
        page.locator('[data-testid="fragmentRuleWhoSaid"]').get_by_text("Любой сказал", exact=True ).click()

    with allure.step("Check that finally became first again"):
        expect(page.locator('[data-testid="fragmentRuleWhoSaid"]')).to_contain_text("Любой сказал")

    with allure.step("Fill (what said)"):
        fill_what_said("someText",page)

    # with allure.step("Check (merge fragments) have value 0,11"):
    #     expect(page.locator('[data-testid="secondsMergeFragmentsText"]').locator('[type="text"]')).to_have_value("0.11") #

    with allure.step("Add all additional terms and click checkboxes in additional params"):
        Additional_terms = ["Искать с начала разговора", "Тегировать только первое совпадение", "Молчание до", "Молчание после", "Время разговора перед фрагментом",
                            "Время разговора после фрагмента", "Длительность перебивания", "Кол-во фрагментов перед этим фрагментом",
                            "Кол-во фрагментов после этого фрагмента", "Время разговора до предыдущего правила", "Кол-во фрагментов до предыдущего правила",
                            "Альтернативный поиск", "Связывать фрагменты"]   # "Связывать фрагменты" changed in https://task.imot.io/browse/DEV-2599

        add_additional_terms(Additional_terms, page)

    with allure.step("Add and delete another fragment"):
        page.locator('[data-testid="fragmentRuleaddFragment"]').click()
        page.locator('[data-testid="fragmentRuleDeleteButton"]').nth(1).click()

    with allure.step("Switch alternative search (who said?) from first to last"):
        page.locator('[data-testid="fragmentRuleBlock"]').locator('[class*="singleValue"]').nth(1).get_by_text("Любой сказал").click()
        page.locator('[data-testid="fragmentRuleBlock"]').get_by_text("Клиент сказал").click()
        page.locator('[data-testid="fragmentRuleBlock"]').get_by_text("Клиент сказал", exact=True).click()
        page.locator('[data-testid="fragmentRuleBlock"]').get_by_text("Сотрудник сказал").click()
        page.locator('[data-testid="fragmentRuleBlock"]').get_by_text("Сотрудник сказал", exact=True).click()
        page.locator('[data-testid="fragmentRuleBlock"]').get_by_text("Любой не сказал").click()
        page.locator('[data-testid="fragmentRuleBlock"]').get_by_text("Любой не сказал", exact=True).click()
        page.locator('[data-testid="fragmentRuleBlock"]').get_by_text("Клиент не сказал").click()
        page.locator('[data-testid="fragmentRuleBlock"]').get_by_text("Клиент не сказал", exact=True).click()
        page.locator('[data-testid="fragmentRuleBlock"]').get_by_text("Сотрудник не сказал").click()
        page.locator('[data-testid="fragmentRuleBlock"]').get_by_text("Сотрудник не сказал", exact=True).click()
        page.locator('[data-testid="fragmentRuleBlock"]').get_by_text("Любой сказал", exact=True).nth(1).click()

    with allure.step("Fill alternative search (what said)"):
        page.locator('[data-testid="fragmentRuleBlock"]').locator('[autocorrect="off"]').nth(1).type("againSomeText", delay=100)
        page.keyboard.press("Enter", delay=100)
        page.wait_for_timeout(500)

    with allure.step("Press (Save) button"):
        page.get_by_role("button", name="Сохранить").click()

    with allure.step("Wait and check snack bar"):
        rules.check_alert("Тег был обновлен")

    with allure.step("Page reload"):
        page.reload()
        page.wait_for_selector('[data-testid="fragmentRuleBlock"]', timeout=wait_until_visible)

    with allure.step("Check that all saved"):
        expect(page.locator('[data-testid="fragmentRuleBlock"]').get_by_text("Любой сказал")).to_have_count(2)
        expect(page.locator('[data-testid="fragmentRuleBlock"]').get_by_text("Искать с начала разговора")).to_have_count(1)
        expect(page.locator('[data-testid="fragmentRuleBlock"]').get_by_text("Тегировать только первое совпадение")).to_have_count(1)

    with allure.step("Delete rule"):
        rules.delete_rule_or_dict()

    with allure.step("Wait and check snack bar"):
        rules.check_alert("Правило удалено")

    with allure.step("Delete group"):
        rules.delete_group()

    with allure.step("Wait and check snack bar"):
        rules.check_alert("Группа удалена")

    with allure.step("Check that deleted"):
        expect(page.get_by_text("99999")).not_to_be_visible(timeout=wait_until_visible) #check no parent group

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN, USER_ID)


@pytest.mark.e2e
@pytest.mark.rules
@allure.title("test_add_rule_inside_group_check_set_tag_block")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("Create rule inside group, check tag block")
def test_add_rule_inside_group_check_set_tag_block(base_url, page: Page) -> None:
    rules = Rules(page)

    with allure.step("Create user"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_USER, PASSWORD)

    with allure.step("Go to url"):
        rules.navigate(base_url)

    with allure.step("Auth with user"):
        rules.auth(LOGIN, PASSWORD)

    with allure.step("Go to markup"):
        rules.click_markup()

    with allure.step("Press (Create group)"):
        rules.press_create_group()

    with allure.step("Check that (Add) button disabled"):
        expect(rules.button_accept).to_be_disabled()

    with allure.step("Add rule name"):
        rules.input_new_group_name("99999")

    with allure.step("Wait and check snack bar"):
        rules.check_alert("Группа добавлена")

    with allure.step("Click at group"):
        page.locator(GROUP_LIST).get_by_text("99999").click()
        page.wait_for_selector('[aria-label="Чтобы добвить тег, выберите или добавьте группу."]', state='hidden')

    with allure.step("Press (Create rule)"):
        rules.press_create_rule()

    with allure.step("Check that (Add) button disabled"):
        expect(rules.button_accept).to_be_disabled()

    with allure.step("Add rule name"):
        rules.input_new_rule_name("set_tags")

    with allure.step("Wait and check snack bar"):
        rules.check_alert("Тег добавлен")

    with allure.step("Check rule name and tag name. Need be the same"):
        page.wait_for_selector(INPUT_TAG_RULE_NAME)
        expect(rules.input_tag_rule_name).to_have_value("set_tags", timeout=wait_until_visible) #check rule
        expect(page.locator('[data-testid="setTagsItem_name"]').locator('[name="name"]')).to_have_value("set_tags", timeout=wait_until_visible) #check tag

    with allure.step("Press button (Add teg)"):
        page.locator('[data-testid="setTagsAddTagButton"]').click()

    with allure.step("Check that teg was added"):
        expect(page.locator('[data-testid="setTagsItem_name"]')).to_have_count(2, timeout=wait_until_visible)
        expect(page.locator('[data-testid="setTagsBlock"]').locator('[aria-label="Добавить значение тега"]')).to_have_count(2, timeout=wait_until_visible)
        expect(page.locator('[data-testid="setTagsDeleteTagButton"]')).to_have_count(2, timeout=wait_until_visible)
        expect(page.locator('[data-testid="setTagsItem_name"]').nth(1).locator('[name="name"]')).to_have_value("set_tags", timeout=wait_until_visible)

    with allure.step("Delete added tag"):
        page.locator('[data-testid="setTagsDeleteTagButton"]').nth(1).click()

    with allure.step("Check that teg deleted"):
        expect(page.locator('[data-testid="setTagsItem_name"]')).to_have_count(1, timeout=wait_until_visible)
        expect(page.locator('[data-testid="setTagsBlock"]').locator('[aria-label="Добавить значение тега"]')).to_have_count(1, timeout=wait_until_visible)
        expect(page.locator('[data-testid="setTagsDeleteTagButton"]')).to_have_count(1, timeout=wait_until_visible)

    with allure.step("Add additional params (tag value)"):
        page.locator('[data-testid="setTagsBlock"]').locator('[aria-label="Добавить значение тега"]').click()
        page.get_by_text("Значение тега", exact=True).click()

    with allure.step("Check that tag value added"):
        expect(page.locator('[name="value"]')).to_have_count(1, timeout=wait_until_visible)

    with allure.step("Fill tag value"):
        page.locator('[name="value"]').fill("tagValue")

    with allure.step("Press (save) button"):
        page.get_by_role("button", name="Сохранить").click()

    with allure.step("Wait and check snack bar"):
        rules.check_alert("Тег был обновлен")

    with allure.step("Page reload"):
        page.reload()
        page.wait_for_selector('[name="value"]')

    with allure.step("Check tag value still exists and have value"):
        expect(page.locator('[name="value"]')).to_have_value("tagValue")
        expect(page.locator('[data-testid="setTagsBlock"]').locator('[aria-label="Убрать значение тега"]')).to_have_count(1, timeout=wait_until_visible)
        expect(page.locator('[data-testid="setTagsDeleteTagButton"]')).to_have_count(1, timeout=wait_until_visible)

    with allure.step("Delete rule"):
        rules.delete_rule_or_dict()

    with allure.step("Wait and check snack bar"):
        rules.check_alert("Правило удалено")

    with allure.step("Delete group"):
        rules.delete_group()

    with allure.step("Wait and check snack bar"):
        rules.check_alert("Группа удалена")

    with allure.step("Check that deleted"):
        expect(page.get_by_text("99999")).not_to_be_visible(timeout=wait_until_visible) #check no parent group

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN, USER_ID)


@pytest.mark.e2e
@pytest.mark.rules
@allure.title("test_add_rule_inside_group_check_tag_sequence")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("test_add_rule_inside_group_check_tag_sequence")
def test_add_rule_inside_group_check_tag_sequence(base_url, page: Page) -> None:
    rules = Rules(page)

    with allure.step("Create user"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_USER, PASSWORD)

    with allure.step("Go to url"):
        rules.navigate(base_url)

    with allure.step("Auth with user"):
        rules.auth(LOGIN, PASSWORD)

    with allure.step("Go to markup"):
        rules.click_markup()

    with allure.step("Press (Create group)"):
        rules.press_create_group()

    with allure.step("Check that (Add) button disabled"):
        expect(rules.button_accept).to_be_disabled()

    with allure.step("Add rule name"):
        rules.input_new_group_name("99999")

    with allure.step("Wait and check snack bar"):
        rules.check_alert("Группа добавлена")

    with allure.step("Click at group"):
        page.locator(GROUP_LIST).get_by_text("99999").click()
        page.wait_for_selector('[aria-label="Чтобы добвить тег, выберите или добавьте группу."]', state='hidden')

    with allure.step("Press (Create rule)"):
        rules.press_create_rule()

    with allure.step("Check that (Add) button disabled"):
        expect(rules.button_accept).to_be_disabled()

    with allure.step("Add rule name"):
        rules.input_new_rule_name("tag_seq")

    with allure.step("Wait and check snack bar"):
        rules.check_alert("Тег добавлен")

    with allure.step("Check that rule created"):
        page.wait_for_selector(INPUT_TAG_RULE_NAME)
        expect(rules.input_tag_rule_name).to_have_value("tag_seq", timeout=wait_until_visible) #check rule

    with allure.step("Add 2 rules for tag sequence and delete one"):
        page.locator(BUTTON_ADD_SEQUENCE).click()

        page.locator(BUTTON_ADD_SEQUENCE).click()
        page.locator(BUTTON_DELETE_SEQUENCE).nth(0).click()

    with allure.step("Check that tag sequence just one"):
        expect(page.locator(BUTTON_DELETE_SEQUENCE)).to_have_count(1)

    with allure.step("Fill (Presence of one of the tags)"):
        page.locator(LIST_PRESENCE_ONE_OF_TAGS).click()
        page.locator(LIST_PRESENCE_ONE_OF_TAGS).get_by_text("tag_seq", exact=True).click()
        page.locator('[class*="styles_ruleItemHeader"]').click()

    with allure.step("Fill (Interval between tags)"):
        page.locator(INPUT_INTERVAL_BETWEEN_TAGS).locator('[type="text"]').fill("1234567890")

    with allure.step("Click on 2 checkboxes"):
        page.locator(CHECK_BOX_ABSENCE_OF_TAGS).click()
        page.locator(CHECK_BOX_REVERSE_LOGIC).click()

    with allure.step("Check that checkboxes checked"):
        expect(page.locator(CHECK_BOX_ABSENCE_OF_TAGS)).to_be_checked()
        expect(page.locator(CHECK_BOX_REVERSE_LOGIC)).to_be_checked()

    with allure.step("Fill (The presence of one of the tags in the specified interval after)"):
        page.locator(LIST_PRESENCE_ONE_OF_TAGS_IN_INTERVAL_AFTER).click()
        page.locator(LIST_PRESENCE_ONE_OF_TAGS_IN_INTERVAL_AFTER).get_by_text("tag_seq", exact=True).click()

    with allure.step("Press (Save) button"):
        page.get_by_role("button", name="Сохранить").click()

    with allure.step("Wait and check snack bar"):
        rules.check_alert("Тег был обновлен")

    with allure.step("Delete tag sequence"):
        page.locator(BUTTON_DELETE_SEQUENCE).click()

    with allure.step("Page reload"):
        page.reload()
        page.wait_for_selector('[data-testid="TagSequenceItem"]', timeout=wait_until_visible)

    with allure.step("Check"):
        expect(page.locator(CHECK_BOX_ABSENCE_OF_TAGS)).to_be_checked()
        expect(page.locator(CHECK_BOX_REVERSE_LOGIC)).to_be_checked()
        expect(page.locator(INPUT_INTERVAL_BETWEEN_TAGS).locator('[type="text"]')).to_have_value("1234567890")
        expect(page.locator('[data-testid="TagSequenceItem"]').get_by_text("tag_seq")).to_have_count(2)

    with allure.step("Delete rule"):
        rules.delete_rule_or_dict()

    with allure.step("Wait and check snack bar"):
        rules.check_alert("Правило удалено")

    with allure.step("Delete group"):
        rules.delete_group()

    with allure.step("Wait and check snack bar"):
        rules.check_alert("Группа удалена")

    with allure.step("Check that deleted"):
        expect(page.get_by_text("99999")).not_to_be_visible(timeout=wait_until_visible) #check no parent group

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN, USER_ID)


@pytest.mark.e2e
@pytest.mark.rules
@allure.title("test_import_group_and_rule_by_admin")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("Precondition: user  importFrom with group 00000 rule 22222 inside with rule 33333 without group")
def test_import_group_and_rule_by_admin(base_url, page: Page) -> None:
    rules = Rules(page)

    with allure.step("Create admin"):
        USER_ID_ADMIN, TOKEN_ADMIN, LOGIN_ADMIN = create_user(API_URL, ROLE_ADMIN, PASSWORD)

    with allure.step("Create user"):
        USER_ID_USER, TOKEN_USER, LOGIN_USER = create_user(API_URL, ROLE_USER, PASSWORD)

    with allure.step("Go to url"):
        rules.navigate(base_url)

    with allure.step("Auth with admin"):
        rules.auth(LOGIN_ADMIN, PASSWORD)

    with allure.step("Go to user"):
        rules.go_to_user(LOGIN_USER)

    with allure.step("Go to markup"):
        rules.click_markup()

    with allure.step("Press (Import rules) button"):
        rules.click_import_rules()

    with allure.step("Select user ImportFrom in modal window"):
        rules.choose_user_import_from("importFrom")

    with allure.step("Check that search string visible"):

        expect(page.locator('[data-testid="markup_importNav_tags"]')).not_to_be_visible()
        expect(page.locator('[data-testid="markup_importNav_dicts"]')).not_to_be_visible()
        expect(page.locator('[data-testid="markup_tags_importSearch}"]')).to_be_visible()
        expect(page.locator('[data-testid="markup_importNav_gpt"]')).not_to_be_visible()

    with allure.step("Import group with rule"):
        page.locator('[class*="CopyMode_copyModeView__popup_"]').locator(CHECKBOX).nth(1).click()
        page.wait_for_timeout(1000)
        page.get_by_role("button", name="Продолжить").click()
        page.wait_for_timeout(2000)

    with allure.step("Import rule"):
        page.locator('[class*="CopyMode_copyModeView__popup_"]').locator(CHECKBOX).nth(3).click()
        page.wait_for_timeout(1000)
        page.get_by_role("button", name="К новым правилам").click()
        page.wait_for_timeout(2000)

    with allure.step("Check that import was successful"):
        expect(page.get_by_text("00000")).to_be_visible(timeout=wait_until_visible)
        expect(page.get_by_text("22222")).to_be_visible(timeout=wait_until_visible)
        expect(page.get_by_text("33333")).to_be_visible(timeout=wait_until_visible)
        expect(page.get_by_text("44444")).to_be_visible(timeout=wait_until_visible)
        expect(page.get_by_text("1 тег")).to_have_count(count=3, timeout=wait_until_visible)

    with allure.step("Click on rule"):
        page.get_by_text("22222").click()

    with allure.step("Delete rule"):
        rules.delete_rule_or_dict()

    with allure.step("Wait for snackbar and check"):
        rules.check_alert("Правило удалено")

    with allure.step("Delete group"):
        rules.button_korzina.first.click()

    with allure.step("Wait for snackbar and check"):
        rules.check_alert("Группа удалена")

    with allure.step("Click on rule"):
        page.get_by_text("44444").click()

    with allure.step("Delete rule"):
        rules.delete_rule_or_dict()

    with allure.step("Wait for snackbar and check"):
        rules.check_alert("Правило удалено")

    with allure.step("Delete group"):
        rules.button_korzina.first.click()

    with allure.step("Wait for snackbar and check"):
        rules.check_alert("Группа удалена")

    with allure.step("Check that deleted"):
        expect(page.get_by_text("00000")).not_to_be_visible(timeout=wait_until_visible)
        expect(page.get_by_text("22222")).not_to_be_visible(timeout=wait_until_visible)
        expect(page.get_by_text("33333")).not_to_be_visible(timeout=wait_until_visible)
        expect(page.get_by_text("44444")).not_to_be_visible(timeout=wait_until_visible)

    with allure.step("Delete admin"):
        delete_user(API_URL, TOKEN_ADMIN, USER_ID_ADMIN)

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN_USER, USER_ID_USER)


@pytest.mark.e2e
@pytest.mark.rules
@allure.title("test_import_group_and_rule_by_manager")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("Precondition: user  importFrom with group 00000 rule 22222 inside with rule 33333 without group")
def test_import_group_and_rule_by_manager(base_url, page: Page) -> None:
    rules = Rules(page)

    with allure.step("Create user"):
        USER_ID_USER, TOKEN_USER, LOGIN_USER = create_user(API_URL, ROLE_USER, PASSWORD)

    with allure.step("Create manager"):
        USER_ID_MANAGER, TOKEN_MANAGER, LOGIN_MANAGER = create_user(API_URL, ROLE_MANAGER, PASSWORD)

    with allure.step("Give user to manager"):
        give_users_to_manager(API_URL, USER_ID_MANAGER, [USER_ID_USER, importFrom_user_id], TOKEN_MANAGER)

    with allure.step("Go to url"):
        rules.navigate(base_url)

    with allure.step("Auth with manager"):
        rules.auth(LOGIN_MANAGER, PASSWORD)

    with allure.step("Go to user"):
        rules.go_to_user(LOGIN_USER)

    with allure.step("Go to markup"):
        rules.click_markup()

    with allure.step("Press (Import rules) button"):
        rules.click_import_rules()

    with allure.step("Select user ImportFrom in modal window"):
        rules.choose_user_import_from("importFrom")

    with allure.step("Check that search string visible"):
        expect(page.locator('[data-testid="markup_importNav_tags"]')).not_to_be_visible()
        expect(page.locator('[data-testid="markup_importNav_dicts"]')).not_to_be_visible()
        expect(page.locator('[data-testid="markup_tags_importSearch}"]')).to_be_visible()
        expect(page.locator('[data-testid="markup_importNav_gpt"]')).not_to_be_visible()

    with allure.step("Import group with rule"):
        page.locator('[class*="CopyMode_copyModeView__popup_"]').locator(CHECKBOX).nth(1).click()
        page.wait_for_timeout(1000)
        page.get_by_role("button", name="Продолжить").click()
        page.wait_for_timeout(2000)

    with allure.step("Import rule"):
        page.locator('[class*="CopyMode_copyModeView__popup_"]').locator(CHECKBOX).nth(3).click()
        page.wait_for_timeout(1000)
        page.get_by_role("button", name="К новым правилам").click()
        page.wait_for_timeout(2000)

    with allure.step("Check that import was successful"):
        expect(page.get_by_text("00000")).to_be_visible(timeout=wait_until_visible)
        expect(page.get_by_text("22222")).to_be_visible(timeout=wait_until_visible)
        expect(page.get_by_text("33333")).to_be_visible(timeout=wait_until_visible)
        expect(page.get_by_text("44444")).to_be_visible(timeout=wait_until_visible)
        expect(page.get_by_text("1 тег")).to_have_count(count=3, timeout=wait_until_visible)

    with allure.step("Click on rule"):
        page.get_by_text("22222").click()

    with allure.step("Delete rule"):
        rules.delete_rule_or_dict()

    with allure.step("Wait for snackbar and check"):
        rules.check_alert("Правило удалено")

    with allure.step("Delete group"):
        rules.button_korzina.first.click()

    with allure.step("Wait for snackbar and check"):
        rules.check_alert("Группа удалена")

    with allure.step("Click on rule"):
        page.get_by_text("44444").click()

    with allure.step("Delete rule"):
        rules.delete_rule_or_dict()

    with allure.step("Wait for snackbar and check"):
        rules.check_alert("Правило удалено")

    with allure.step("Delete group"):
        rules.button_korzina.first.click()

    with allure.step("Wait for snackbar and check"):
        rules.check_alert("Группа удалена")

    with allure.step("Check that deleted"):
        expect(page.get_by_text("00000")).not_to_be_visible(timeout=wait_until_visible)
        expect(page.get_by_text("22222")).not_to_be_visible(timeout=wait_until_visible)
        expect(page.get_by_text("33333")).not_to_be_visible(timeout=wait_until_visible)
        expect(page.get_by_text("44444")).not_to_be_visible(timeout=wait_until_visible)

    with allure.step("Delete manager"):
        delete_user(API_URL, TOKEN_MANAGER, USER_ID_MANAGER)

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN_USER, USER_ID_USER)


@pytest.mark.e2e
@pytest.mark.rules
@allure.title("test_import_rule_disabled_for_user")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("test_import_rule_disabled_for_user")
def test_import_rule_disabled_for_user(base_url, page: Page) -> None:
    rules = Rules(page)

    with allure.step("Create user"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_USER, PASSWORD)

    with allure.step("Go to url"):
        rules.navigate(base_url)

    with allure.step("Auth with user"):
        rules.auth(LOGIN, PASSWORD)

    with allure.step("Go to markup"):
        rules.click_markup()

    with allure.step("Check that button for import not visible"):
        expect(page.locator(BUTTON_IMPORT_RULES)).not_to_be_visible()

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN, USER_ID)


@pytest.mark.e2e
@pytest.mark.rules
@allure.title("test_compare_rules_by_user")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("User has three rules with different parameters. when he switch between them, all parameters changing.")
def test_compare_rules_by_user(base_url, page: Page) -> None:
    rules = Rules(page)

    with allure.step("Go to url"):
        rules.navigate(base_url)

    with allure.step("Auth with user for check comparelogin"):
        rules.auth(USER_FOR_CHECK, PASSWORD)

    with allure.step("Go to markup"):
        rules.click_markup()

    with allure.step("Go to first rule"):
        page.get_by_text("firstrule").click()
        page.wait_for_selector('[data-testid="fragmentRuleBlock"]')

    with allure.step("Check filters and other inside rule"):
        expect(page.locator('[aria-label="Remove >100"]')).to_be_visible(timeout=wait_until_visible)
        expect(page.locator('[aria-label="Remove Словарь: firstdict"]')).to_be_visible()
        expect(page.locator('[data-testid="TagSequenceItem"]').locator('[aria-label="Remove firstrule"]')).to_have_count(2)
        expect(page.locator('[data-testid="intervalBetweenTags"]').locator('[value=">100"]')).to_have_count(1)
        expect(page.locator('[data-testid="setTagsBlock"]').locator('[name="name"]')).to_have_value("firstrule")
        expect(page.locator('[data-testid="setTagsBlock"]').locator('[name="value"]')).to_have_value("firstrulevalue")

    with allure.step("Change rule"):
        page.get_by_text("secondrule").click()
        page.wait_for_timeout(4000)

    with allure.step("Check filters and other inside rule was changed"):
        expect(page.locator('[aria-label="Remove >2222"]')).to_be_visible()
        expect(page.locator('[aria-label="Remove Словарь: seconddict"]')).to_be_visible()
        expect(page.locator('[data-testid="TagSequenceItem"]').locator('[aria-label="Remove secondrule"]')).to_have_count(2)
        expect(page.locator('[data-testid="intervalBetweenTags"]').locator('[value=">2222"]')).to_have_count(1)
        expect(page.locator('[data-testid="setTagsBlock"]').locator('[name="name"]')).to_have_value("secondrule")
        expect(page.locator('[data-testid="setTagsBlock"]').locator('[name="value"]')).to_have_value("secondrulevalue")

    with allure.step("Change rule"):
        page.get_by_text("thirdrule").click()
        page.wait_for_timeout(4000)

    with allure.step("Check that tagname still the same, but tagvalue changed"):
        expect(page.locator('[aria-label="Remove firstrule: firstrulevalue"]')).to_be_visible()
        expect(page.locator('[aria-label="Remove word"]')).to_be_visible()
        expect(page.locator('[data-testid="setTagsBlock"]').locator('[name="name"]')).to_have_value("secondrule")
        expect(page.locator('[data-testid="setTagsBlock"]').locator('[name="value"]')).to_have_value("thirdrulevalue")


@pytest.mark.e2e
@pytest.mark.rules
@allure.title("test_check_rules_search_and_sort")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("test_check_rules_search_and_sort")
def test_check_rules_search_and_sort(base_url, page: Page) -> None:
    rules = Rules(page)

    with allure.step("Create user"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_USER, PASSWORD, create_many_rules=True)

    with allure.step("Go to url"):
        rules.navigate(base_url)

    with allure.step("Auth with user"):
        rules.auth(LOGIN, PASSWORD)

    with allure.step("Go to markup"):
        rules.click_markup()

    with allure.step("Filter rules by sort"):
        rules.input_search.nth(1).type("test ", delay=10)

    with allure.step("Check that button for import not visible"):
        expect(rules.input_search.nth(1)).to_have_value("test ")

    with allure.step("Clear search"):
        rules.input_search.nth(1).clear()

    with allure.step("Filter rules by sort"):
        rules.input_search.nth(1).type("AUTO", delay=10)

    with allure.step("Check that button for import not visible"):
        expect(page.get_by_text("auto_rule", exact=True)).to_be_visible()

    with allure.step("Clear search"):
        rules.input_search.nth(1).clear()

    with allure.step("Filter rules by sort"):
        rules.input_search.nth(1).type("many", delay=10)

    with allure.step("Check that button for import not visible"):
        expect(page.get_by_text("auto_rule", exact=True)).not_to_be_visible()

    with allure.step("Change sort"):
        rules.change_sort("Сначала обновленные", "По алфавиту")

    with allure.step("Check first rule name"):
        rules.assert_first_group_name("AT_many_rules1")

    with allure.step("Change sort"):
        rules.change_sort("По алфавиту", "По алфавиту с конца")

    with allure.step("Check first rule name"):
        rules.assert_first_group_name("AT_many_rules5")

    with allure.step("Change sort"):
        rules.change_sort("По алфавиту с конца", "Сначала новые")

    with allure.step("Check first rule name"):
        rules.assert_first_group_name("AT_many_rules5")

    with allure.step("Change sort"):
        rules.change_sort("Сначала новые", "Сначала старые")

    with allure.step("Check first rule name"):
        rules.assert_first_group_name("AT_many_rules1")

    with allure.step("Change sort"):
        rules.change_sort("Сначала старые", "Сначала обновленные")

    with allure.step("Check first rule name"):
        rules.assert_first_group_name("AT_many_rules5")

    with allure.step("Change sort"):
        rules.change_sort("Сначала обновленные", "Сначала не обновленные")

    with allure.step("Check first rule name"):
        rules.assert_first_group_name("AT_many_rules1")

    with allure.step("Change sort"):
        rules.change_sort("Сначала не обновленные", "По алфавиту")

    with allure.step("Check first rule name"):
        rules.assert_first_group_name("AT_many_rules1")

    page.locator('[data-testid="test"]').locator(CHECKBOX).first.click()
    page.wait_for_timeout(500)

    with allure.step("Check that button for import not visible"):
        expect(page.get_by_text("auto_rule", exact=True)).not_to_be_visible()
        expect(page.locator('[class*="Mui-checked"]')).to_have_count(6)

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN, USER_ID)

