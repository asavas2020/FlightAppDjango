from rest_framework import serializers
from .models import Flight, Passenger, Reservation



class FlightSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Flight
        fields = (
            "flight_number",
            "operating_airlines",
            "departure_city",
            "arrival_city",
            "date_of_departure",
            "etd"
        )

class PassengerSerializer(serializers.ModelSerializer):

    class Meta:
        fields = "__all__"


class ReservationSerializer(serializers.ModelSerializer):

    Passenger = PassengerSerializer(many = True, required = True)
    flight = serializers.StringRelatedField() # default read_only true
    flight_id = serializers.IntegerField(write_only = True)
    user = serializers.StringRelatedField() # default read_only true
    user_id = serializers.IntegerField(write_only = True, required = False)

    class Meta:
        model = Reservation
        fields = (
            "id"
            "flight" # get
            "flight_id" # post
            "user" # get
            "user_id" # post
            "Passenger"
        )

    def create(self, validated_data):
        passenger_data = validated_data.pop("Passenger")
        validated_data["user_id"] = self.context["request"].user.id 
        reservation = Reservation.objects.create(**validated_data)

        for passenger in passenger_data:
            pas = Passenger.objects.create(**passenger)
            reservation.passenger.add(pas)
        reservation.save()
        return reservation

class StaffFlightSerializer(serializers.ModelSerializer):

    reservation = ReservationSerializer(many = True, read_only = True)

    class Meta:
        model = Flight
        fields = "__all__"
