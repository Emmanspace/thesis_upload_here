from rest_framework import serializers

from .models import History, Category, Notification, Departments, totalSlots, availableSlots, parkingSlots, real_time, historytab, User, UserProfile#, userEdit
# from .models import Availability

class announcementSerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields = ('id', 'title')

class HistorySerializers(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = (
            'id',
            'intent',
            'start',
            'end',
            'duration',
            'date_at',
            'date_formatted',
            'Total_parking_Slots',
            'Vehicles_Parked',
            'Available_slots'
        )

class DashboardSerializers(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = (
            'id',
            'intent',
            'start',
            'end',
            'duration',
            'date_at',
            'date_formatted',
            'Total_parking_Slots',
            'Vehicles_Parked',
            'Available_slots'
        )

class notificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields  = (
            'notification',
            'created_at_formatted'
        )


#added
# for dashboard api
class totalSlot_Serializer(serializers.ModelSerializer):
    class Meta:
        model = totalSlots
        fields = ('total_slots',)

class availableSlots_Serializer(serializers.ModelSerializer):
    class Meta:
        model = availableSlots
        fields = ('available_slots',)

class parkingSlots_Serializer(serializers.ModelSerializer):
    class Meta:
        model = parkingSlots
        fields = ('parking_slots',)

# added for mongoDB (updated)
# this is for test run
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Departments
        fields = ('DepartmentId', 'DepartmentName')


# for jairo's db
class real_time_serializer(serializers.ModelSerializer):
    class Meta:
        model = real_time
        fields = (
            'confidence',
            'plate',
            'date_formatted',
            'time'
        )

# for historytab 
class historyserializer(serializers.ModelSerializer):
    class Meta:
        model = historytab
        fields= (
            'intent',
            'start',
            'end',
            'duration',
            'date_formatted'
        )


# for authentication1
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 
            'user_email',
            'username',
            'user_first_name',
            'user_last_name',
            'user_plate'
            'user_is_active',
            'user_is_staff', 
            'user_date_joined']
        
        # extra_kwargs = {'user': {'required': False}}

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = User.objects.filter(email=email).first()

            if user and user.check_password(password):
                return {'user': user}
            
        raise serializers.ValidationError('Incorrect email or password')
# end of authentication1

# authentication2
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 
            'password'
            )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user=User.Objects.create_user(**validated_data)
        return user
# end of auth2

# for profile update
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'plate',
            'password'
            )
# end of profile update

# for test run (2:26am)
class documentSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    
# enf of test run

# 4-23
# class userEditSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = userEdit
#         fields = (
#             '_id',
#             'username',
#            'first_name',
#             'last_name',
#             'email' 

#         )
# 4-23