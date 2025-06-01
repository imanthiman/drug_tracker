import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import DrugLabelSerializer, SideEffectsSerializer

class DrugInfoView(APIView):
    def get(self, request):
        drug_name = request.GET.get("name")
        if not drug_name:
            return Response({"error": "Drug name is required."}, status=status.HTTP_400_BAD_REQUEST)

        url = f"https://api.fda.gov/drug/label.json?search=openfda.generic_name:\"{drug_name}\"&limit=1"
        try:
            fda_response = requests.get(url)
            data = fda_response.json()
            result = data['results'][0]

            raw_data = {
                "active_ingredient": result.get("active_ingredient", ["N/A"])[0],
                "dosage_form": result.get("dosage_form", ["N/A"])[0],
                "purpose": result.get("purpose", ["N/A"])[0],
            }

            serializer = DrugLabelSerializer(data=raw_data)

            if serializer.is_valid():
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=400)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
class SideEffectsView(APIView):
    def get(self, request):
        drug_name = request.GET.get("drug")
        if not drug_name:
            return Response({"error": "Drug name is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        url = f'https://api.fda.gov/drug/event.json?search=patient.drug.medicinalproduct:"{drug_name}"&limit=5'

        try:
            fda_response = requests.get(url)
            data = fda_response.json()
            results = data.get("results", [])

            side_effects = []

            for report in results:
                reactions = report.get('patient', {}).get("reaction", [])
                for reaction in reactions:
                    side_effects.append(reaction.get("reactionmeddrapt", "Unknown"))
            
            formatted_data = {
                "drug": drug_name,
                "side_effects": list(set(side_effects))
            }

            serializer = SideEffectsSerializer(data=formatted_data)
            if serializer.is_valid():
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=400)
            
        except Exception as e:
            return Response({"error": str(e)}, status=500)