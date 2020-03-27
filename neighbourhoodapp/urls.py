from django.urls import path
from .views import UserCreate, UserProfile, CreateNeighbourhood, SpecificHood, UserList, DeleteUser, EditHoodInfo, \
    DeleteHood, \
    HoodBusiness, BusinessList, UpdateBusiness, Contacts, UpdateContacts, ContactList, UserPosts, LoginView, AddHoodAdmin

urlpatterns = [
    path('user_registration/', UserCreate.as_view(), name='user_create'),
    path("login/", LoginView.as_view(), name="login"),
    path('profile/<int:pk>/', UserProfile.as_view(), name='profile_update'),
    path('admin/<int:pk>/create_neighbourhood/', CreateNeighbourhood.as_view(), name='neighbourhood'),
    path('get_neighbourhood/<int:pk>/', SpecificHood.as_view(), name='specific_hood'),
    path('all_users/', UserList.as_view(), name='all_users'),
    path('admin/<int:id>/delete_user/<int:pk>/', DeleteUser.as_view(), name='delete_user'),
    path('admin/<int:id>/edit_hood_info/<int:pk>/', EditHoodInfo.as_view(), name="edit_hood_info"),
    path('admin/<int:id>/delete_hood/<int:pk>/', DeleteHood.as_view(), name="delete_hood"),
    path('neighbourhood/<int:pk>/create_business/', HoodBusiness.as_view(), name="create_business"),
    path('business_list/<int:pk>/', BusinessList.as_view(), name="business_list"),
    path('update_business_info/<int:pk>/business/<name>/', UpdateBusiness.as_view(), name="update_business"),
    path('create_contacts/<int:pk>/', Contacts.as_view(), name="contacts"),
    path('update_contacts/<int:pk>/service/<service_name>/', UpdateContacts.as_view(), name="update_contacts"),
    path('contact_list/<int:pk>/', ContactList.as_view(), name="contact_list"),
    path('add_post/<int:pk>/', UserPosts.as_view(), name='add_post'),
    path('select_hood_admin/<int:id>/user/<int:pk>/', AddHoodAdmin.as_view(), name="select_hood_admin"),
]
