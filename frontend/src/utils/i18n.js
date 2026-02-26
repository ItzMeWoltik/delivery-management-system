let currentLang = 'EN';

const translations = {
  EN: {
    email: 'Email',
    password: 'Password',
    login: 'Login',
    register: 'Register',
    customer: 'Customer',
    courier: 'Courier',
    from_address: 'From Address',
    to_address: 'To Address',
    create_order: 'Create Order',
    order_id: 'Order ID',
    check_status: 'Check Status',
    status: 'Status',
    description: 'Description',
    create_ticket: 'Create Ticket',
    accept: 'Accept',
    start: 'Start',
    complete: 'Complete',
    update_location: 'Update Location',
    force_cancel: 'Force Cancel',
  },
  UA: {
    email: 'Електронна пошта',
    password: 'Пароль',
    login: 'Увійти',
    register: 'Зареєструватися',
    customer: 'Клієнт',
    courier: 'Кур\'єр',
    from_address: 'З адреси',
    to_address: 'До адреси',
    create_order: 'Створити замовлення',
    order_id: 'ID замовлення',
    check_status: 'Перевірити статус',
    status: 'Статус',
    description: 'Опис',
    create_ticket: 'Створити тікет',
    accept: 'Прийняти',
    start: 'Почати',
    complete: 'Завершити',
    update_location: 'Оновити локацію',
    force_cancel: 'Примусово скасувати',
  },
};

export const translate = (key) => translations[currentLang][key] || key;

export const setLanguage = (lang) => {
  currentLang = lang;
};