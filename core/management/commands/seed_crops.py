from django.core.management.base import BaseCommand
from core.models import Crop, Livestock

class Command(BaseCommand):
    help = 'Seed the database with initial crop and livestock data for Uganda'

    def handle(self, *args, **kwargs):
        crops = [
            {
                'name': 'Maize (Longe 5)',
                'ideal_soil': 'loamy',
                'planting_season': 'Early March / August - September',
                'expected_yield_per_acre': '25-35 bags (50kg bags)',
                'description': 'Uganda\'s most important cereal crop for food security and animal feed.',
                'factors_favouring': 'Thrives in Uganda\'s tropical climate with two rainy seasons. Optimal temperatures 18-30°C. Needs well-distributed rainfall 600-1200mm. Well-drained loamy soils with good organic matter. Responds well to nitrogen fertilizer.',
                'layman_knowledge': 'Plant maize during the rainy season. Make planting holes about 60cm apart in rows 90cm apart. Put 2-3 seeds per hole. Thin to one strong plant after germination. Remove weeds when maize is knee-high (first 4-6 weeks). Apply manure at planting time for better harvest. Harvest when cobs turn golden-brown.',
                'preferred_regions': 'Kampala, Mubende, Jinja, Masaka, Mbale, Mukono, Soroti',
                'best_for_farmer_type': 'smallholder',
                'market_potential': 'Staple food with consistent demand. Prices range from UGX 1,500-2,500 per kg. Highest prices during dry seasons. Good for both home consumption and market.',
                'planting_instructions': '1. Clear and plough field 2 weeks before rains 2. Plant at onset of rains 3. Space holes 60x90cm 4. 2-3 seeds per hole, 3cm deep 5. Thin to 1 plant at 3 weeks 6. Weed at 4 and 8 weeks 7. Apply manure at planting, top-dress at knee-high',
                'pest_disease_management': 'Armyworm: Hand pick or use neem. Fall armyworm: Early detection and spray with recommended insecticides. Stem borer: Destroy crop residues after harvest. Maize streak virus: Plant resistant varieties like Longe 5.'
            },
            {
                'name': 'Matooke (Plantain Bananas)',
                'ideal_soil': 'loamy',
                'planting_season': 'Year-round with slight increase in rainy seasons',
                'expected_yield_per_acre': '400-800 bunches per year',
                'description': 'Uganda\'s staple food in Central and Western regions. Main source of carbohydrates.',
                'factors_favouring': 'Needs deep fertile soils rich in organic matter. High rainfall (1500mm+) with good distribution. Warm temperatures (20-30°C). Protection from strong winds essential. Responds excellently to composted manure and mulch.',
                'layman_knowledge': 'Matooke thrives where the soil is very rich. Dig a big hole (1m x 1m) and fill with lots of well-rotted manure before planting. Apply mulch (dry banana leaves, grass) around the plant but not touching the stem. Space plants 3m apart. Keep plants weed-free. Remove dead leaves. Apply manure annually for continuous production. Harvest bunches when fingers are plump and yellow.',
                'preferred_regions': 'Masaka, Mukono, Fort Portal, Mbarara, Kabale',
                'best_for_farmer_type': 'smallholder',
                'market_potential': 'Staple food with high daily demand. A bunch sells for UGX 5,000-20,000 depending on size. Best markets in urban centers like Kampala, Entebbe, Jinja.',
                'planting_instructions': '1. Select healthy sword suckers from productive plants 2. Dig hole 1x1x1m 3. Fill with 50kg compost 4. Plant sucker at same soil level 5. Space 3x3m 6. Mulch heavily with banana leaves',
                'pest_disease_management': 'Banana weevil: Clean planting material and crop rotation. Black Sigatoka: Remove and burn infected leaves. Nematodes: Apply compost and rotate crops.'
            },
            {
                'name': 'Robusta Coffee',
                'ideal_soil': 'loamy',
                'planting_season': 'April - June (main season)',
                'expected_yield_per_acre': '1500-2500 kg dried beans',
                'description': 'Uganda\'s leading agricultural export crop. High value product.',
                'factors_favouring': 'Best at altitudes below 1500m. Volcanic soils with good drainage. High rainfall (2000-3000mm). Shade trees recommended. Temperature 20-24°C ideal. Soil pH 5.5-6.5.',
                'layman_knowledge': 'Coffee is an investment for the long term. Space trees 2.5-3m apart. Plant under shade trees (Albida, Markhamia). Prune old branches to encourage new growth and berries. Weed regularly for first 2 years. Feed with compost yearly. The cherry turns red when ripe - that\'s when to pick. Dry the cherries properly before selling.',
                'preferred_regions': 'Mbale, Jinja, Mukono, West Nile, Kasese',
                'best_for_farmer_type': 'commercial',
                'market_potential': 'High export value. Prices UGX 3,000-6,000 per kg dried cherries. Cooperative societies offer better prices. Can sell green or roasted.',
                'planting_instructions': '1. Plant nursery 6-8 months before field 2. Prepare holes 60x60x60cm 3. Add manure and topsoil 4. Space plants 2.5-3m 5. Plant shade trees first 6. Prune annually for open canopy',
                'pest_disease_management': 'Coffee berry borer: Harvest ripe cherries completely and clean farm. Coffee leaf rust: Prune for air circulation and use resistant varieties.'
            },
            {
                'name': 'Beans (Kidney Beans & Pinto)',
                'ideal_soil': 'loamy',
                'planting_season': 'March - April and September - October',
                'expected_yield_per_acre': '8-15 bags (50kg bags)',
                'description': 'High-protein crop important for household nutrition and income.',
                'factors_favouring': 'Moderate rainfall 750-1000mm. Grows best in loamy soils. Quick maturing (3-4 months). Nitrogen-fixing crop improves soil. Temperature 15-27°C optimal.',
                'layman_knowledge': 'Plant beans early in the rainy season. Space rows 45cm apart and seeds 20cm in rows. Don\'t overwater - beans hate wet feet. Weed at 3 and 6 weeks. Harvest pods when they turn golden-brown and papery. Dry on mats or hang bundles. Store in cool, dry place. Beans pair well with maize in crop rotation.',
                'preferred_regions': 'All regions, especially Mubende, Kabale, Kisoro, Mbarara',
                'best_for_farmer_type': 'smallholder',
                'market_potential': 'Always in demand. UGX 2,000-4,000 per kg. Prices highest before harvest season. Good for both market and home nutrition.',
                'planting_instructions': '1. Plant at onset of rains 2. Rows 45cm apart 3. Seeds 20cm in row, 3-5cm deep 4. 2 seeds per hole 5. Thin to one plant at 2 weeks 6. Weed at 3 and 6 weeks',
                'pest_disease_management': 'Bean aphids: Use soapy water or neem spray. Bean rust: Plant early, remove infected leaves. Anthracnose: Use certified disease-free seed.'
            },
            {
                'name': 'Cassava',
                'ideal_soil': 'sandy',
                'planting_season': 'Beginning of rains (March and September)',
                'expected_yield_per_acre': '10-20 tons fresh roots',
                'description': 'Drought-resistant, versatile crop for food security and income.',
                'factors_favouring': 'Tolerates poor soils and low rainfall. Prefers warm climate 25-30°C. Well-drained soils critical to prevent rot. Can grow on marginal lands unsuitable for other crops.',
                'layman_knowledge': 'Cassava is very forgiving. Plant stem cuttings (20cm) at an angle or flat. Space 1m x 1m or 0.8m x 0.8m. Plant during rainy season. Very little maintenance needed - rarely gets serious pests. Weeds competitors in first 3 months. Can stay in ground 8-24 months. Harvest by digging around plant carefully. Wash roots clean.',
                'preferred_regions': 'Northern regions, Eastern regions, Gulu, Lira, Soroti, Amuria',
                'best_for_farmer_type': 'smallholder',
                'market_potential': 'Food security crop with stable market. Fresh roots UGX 300-800 per kg. Can process to cassava flour (UGX 1,500-3,000 per kg) for better price.',
                'planting_instructions': '1. Select healthy brown stems from mature plants 2. Cut 20-30cm cuttings with 5-7 nodes 3. Plant 2/3 in soil at angle 4. Space 1x1m 5. Plant at onset of rains',
                'pest_disease_management': 'Cassava mosaic virus: Use resistant varieties like NASE 14. Cassava brown streak: Plant clean material and remove infected plants.'
            },
            {
                'name': 'Groundnuts (Peanuts)',
                'ideal_soil': 'sandy',
                'planting_season': 'April - May and October - November',
                'expected_yield_per_acre': '1-2 tons',
                'description': 'Protein-rich crop important for nutrition and income. Used for oil and food.',
                'factors_favouring': 'Well-drained sandy loam soils. Low rainfall requirement (500-750mm). Warm growing season. Grows quickly (90-120 days). Benefits from potassium fertilizer.',
                'layman_knowledge': 'Groundnuts like loose soil. Plough well before planting. Plant at start of rains. Space rows 30cm apart and seeds 20cm in rows. Weed at 4 and 8 weeks. When leaves turn yellow and flowers fall, the groundnuts are forming underground. Dig carefully - nuts stay in the pod in the soil. Dry thoroughly before storing.',
                'preferred_regions': 'Arua, Mbarara, Masaka, Mukono, all regions',
                'best_for_farmer_type': 'smallholder',
                'market_potential': 'Good nutrition and income. Shelled nuts UGX 2,000-4,000 per kg. Oil mills offer bulk prices. Roasted nuts sell well in markets.',
                'planting_instructions': '1. Plant at start of rains 2. Rows 30-45cm 3. Seeds 15-20cm apart, 5cm deep 4. 2 seeds per hole 5. Thin to one plant 6. Weed at 4 and 8 weeks',
                'pest_disease_management': 'Aphis: Early planting reduces damage. Leaf spot: Rotate crops and remove debris. Termites: Dig trenches and destroy mounds.'
            },
            {
                'name': 'Irish Potatoes',
                'ideal_soil': 'loamy',
                'planting_season': 'March - April and August - September',
                'expected_yield_per_acre': '15-25 tons',
                'description': 'Commercial vegetable crop with good market demand.',
                'factors_favouring': 'Cool highlands 1500-2500m elevation. Well-drained soils. Regular rainfall 800-1000mm. Responds well to manure and NPK fertilizer.',
                'layman_knowledge': 'Use certified disease-free seed potatoes. Plant on ridges in cool season. Apply plenty of manure before planting. Spray for late blight if rains are heavy. Harvest after vines die down.',
                'preferred_regions': 'Kabale, Kisoro, Kanungu, Mbarara highlands',
                'best_for_farmer_type': 'commercial',
                'market_potential': 'High value commercial crop. UGX 800-2,000 per kg. Urban markets pay premium. Good road access important for this crop.',
                'planting_instructions': '1. Cut seed potatoes 50-70g with 2-3 eyes 2. Plant on ridges 75cm apart 3. Tubers 30cm apart in row 4. Earthing-up at 4 weeks',
                'pest_disease_management': 'Late blight: Early spray with fungicides, plant resistant varieties. Bacterial wilt: Rotate crops, use clean seed.'
            },
            {
                'name': 'Tomatoes',
                'ideal_soil': 'loamy',
                'planting_season': 'Year-round, peak dry seasons',
                'expected_yield_per_acre': '15-25 tons',
                'description': 'High-value vegetable crop important for nutrition and income.',
                'factors_favouring': 'Warm season crop. Loamy soils with good drainage. Needs consistent water. Temperature 20-30°C. Responds excellently to compost and manure.',
                'layman_knowledge': 'Start seeds in nursery, transplant at 4-6 leaf stage. Space plants 60cm x 60cm. Plant at start of dry season for best prices. Water regularly - tomatoes need consistent moisture. Support plants with sticks. Spray for late blight in wet seasons. Pick mature green or fully ripe fruits.',
                'preferred_regions': 'All regions, year-round production',
                'best_for_farmer_type': 'commercial',
                'market_potential': 'Very high demand. Prices UGX 1,000-4,000 per kg depending on season. Off-season planting (dry season) gets best prices.',
                'planting_instructions': '1. Nursery for 4-6 weeks 2. Transplant 60x60cm spacing 3. Stake at transplanting 4. Prune suckers for better air flow',
                'pest_disease_management': 'Late blight: Spray protective fungicides. Bacterial wilt: Rotate with non-solanaceous crops. Fruit worms: Hand pick or use Bt.'
            },
        ]

        livestock = [
            {
                'name': 'Local Chickens',
                'description': 'Indigenous chicken breeds well-adapted to Ugandan conditions. Low input, high resilience.',
                'best_regions': 'All regions, especially rural areas',
                'expected_income': 'UGX 15,000-30,000 per mature bird',
                'housing_requirements': 'Simple raised house with good ventilation, perches for roosting, nesting boxes.',
                'feeding_guide': 'Free range during day, supplement with kitchen scraps, maize bran, sorghum, kitchen waste. Water always available.',
                'health_tips': 'Vaccinate against Newcastle disease every 3-4 months. Deworm every 3 months. Keep house clean and dry.',
                'market_info': 'Excellent demand. Birds sell at markets, to restaurants, and for ceremonies. Eggs UGX 300-500 each.',
                'best_for_farmer_type': 'smallholder'
            },
            {
                'name': 'Improved Chicken Breeds (Kuroiler)',
                'description': 'Dual-purpose breed for meat and eggs. Fast growing and high egg production.',
                'best_regions': 'All regions, good for peri-urban areas',
                'expected_income': 'UGX 25,000-50,000 per bird at 4-5 months',
                'housing_requirements': 'More intensive housing needed, better protection from predators. Good ventilation and lighting.',
                'feeding_guide': 'Requires balanced commercial feed or good quality homemade feed. 100-150g per bird per day.',
                'health_tips': 'Full vaccination program: Marek\'s, Newcastle, Gumboro, Fowl pox. Regular deworming.',
                'market_info': 'Meat in high demand. Eggs have premium market. Good restaurant and butcher supply.',
                'best_for_farmer_type': 'commercial'
            },
            {
                'name': 'Local Cattle (Ankole, Nganda)',
                'description': 'Indigenous breeds adapted to local conditions. Resistant to many diseases.',
                'best_regions': 'Western region (Ankole), Central region, Eastern region',
                'expected_income': 'UGX 800,000-3,000,000 per mature animal',
                'housing_requirements': 'Night kraal for protection. Simple shade structures. Water trough.',
                'feeding_guide': 'Mostly grazing. Supplement with crop residues (maize stover, banana peels). Mineral lick important.',
                'health_tips': 'Regular dipping for ticks. Vaccinate against FMD, CBPP, anthrax. Deworm every 3-6 months.',
                'market_info': 'Very good market. Live animals sold at weekly markets. Meat processing growing industry.',
                'best_for_farmer_type': 'smallholder'
            },
            {
                'name': 'Goats (Local & Boer)',
                'description': 'Small ruminants, easy to keep, good for income and home consumption.',
                'best_regions': 'All regions, especially dry areas of Northern and Eastern Uganda',
                'expected_income': 'UGX 150,000-500,000 per goat',
                'housing_requirements': 'Simple raised shelter. Protection from rain and predators. Good drainage.',
                'feeding_guide': 'Browse on shrubs and trees. Supplement with crop residues. Mineral salt essential.',
                'health_tips': 'Vaccinate against PPR annually. Deworm every 3 months. Foot bath regularly.',
                'market_info': 'Good consistent demand. Muslims provide seasonal market peaks. Meat preferred by many cultures.',
                'best_for_farmer_type': 'smallholder'
            },
            {
                'name': 'Pigs',
                'description': 'Fast growing, high reproduction. Excellent converter of kitchen and farm waste.',
                'best_regions': 'All regions, particularly Central and Eastern',
                'expected_income': 'UGX 300,000-800,000 per pig at 6-8 months',
                'housing_requirements': 'Sturdy pens with concrete floor for cleaning. Separate farrowing area. Good ventilation.',
                'feeding_guide': 'Kitchen waste, brewery by-products, maize bran, forage. Balanced diet for fast growth.',
                'health_tips': 'Vaccinate against ASF and FMD. Deworm regularly. Keep pens clean and dry.',
                'market_info': 'Very high demand in urban areas. Pork joints and restaurants provide steady market.',
                'best_for_farmer_type': 'commercial'
            },
            {
                'name': 'Bees (Honey Production)',
                'description': 'Low input, high value. No land competition. Pollination benefits crops.',
                'best_regions': 'All regions, areas with good tree cover and flowering plants',
                'expected_income': 'UGX 5,000-15,000 per kg honey. 10-20kg per hive per harvest.',
                'housing_requirements': 'Kenyan top bar hives or Langstroth hives. Place in shaded area away from home.',
                'feeding_guide': 'Natural forage best. Plant bee-friendly trees: Calliandra, Leucaena, fruit trees.',
                'health_tips': 'Hive hygiene. Protect from ants. Harvest carefully to avoid absconding.',
                'market_info': 'Honey always in demand. UGX 5,000-20,000 per kg depending on quality. Health food trend growing.',
                'best_for_farmer_type': 'smallholder'
            },
        ]

        for crop_data in crops:
            crop, created = Crop.objects.update_or_create(
                name=crop_data['name'],
                defaults=crop_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"✓ Created crop: {crop.name}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"✓ Updated crop: {crop.name}"))

        for livestock_data in livestock:
            livest, created = Livestock.objects.update_or_create(
                name=livestock_data['name'],
                defaults=livestock_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"✓ Created livestock: {livest.name}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"✓ Updated livestock: {livest.name}"))
        
        self.stdout.write(self.style.SUCCESS(f"\n✓ Successfully seeded {len(crops)} Ugandan crops and {len(livestock)} livestock with AI knowledge!"))
