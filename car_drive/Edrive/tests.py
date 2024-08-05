from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import MyCar, FuelRecord, CarModel
from django.utils import timezone
from datetime import timedelta

class UserLevelUpTestCase(TestCase):
    def setUp(self):
        User = get_user_model()
        # ユーザーを作成
        self.user = User.objects.create(user_name='testuser', password='testpassword')

        # CarModel インスタンスを作成
        self.car_model = CarModel.objects.create(
            car_model_name='Test Model',
            engine_type='gasoline',
            color='red',
            average_fuel_efficiency=15.0
        )

        # MyCar インスタンスを作成
        self.my_car = MyCar.objects.create(
            user=self.user,
            car_model=self.car_model,
            target_fuel_efficiency=12.0  # 目標燃費
        )

        # FuelRecord を 6 件作成（5 件でレベルアップ）
        for i in range(6):
            FuelRecord.objects.create(
                my_car=self.my_car,
                #date=timezone.now() - timedelta(days=i),
                distance=100,
                fuel_amount=8,
                fuel_efficiency=12.0 + i  # 目標燃費を超える
            )

    def test_user_level_up(self):
        # ユーザーのレベルアップ前の状態を確認
        user = get_user_model().objects.get(pk=self.user.pk)
        self.assertEqual(user.driver_level, 1)
        self.assertEqual(user.target_achievement_count, 0)  # 6 件中 1 件が残る

        # 処理を実行（通常はビューで処理される）
        # ここでは手動で更新する仮定の処理を追加
        target_achievement_count = user.target_achievement_count
        for record in FuelRecord.objects.all():
            if record.fuel_efficiency is not None and record.my_car.target_fuel_efficiency is not None:
                if record.fuel_efficiency >= record.my_car.target_fuel_efficiency:
                    target_achievement_count += 1

        if target_achievement_count >= 5:
            user.driver_level += 1
            user.target_achievement_count = target_achievement_count - 5
        else:
            user.target_achievement_count = target_achievement_count

        user.save()

        # 更新後のユーザー情報を確認
        user.refresh_from_db()
        self.assertEqual(user.driver_level, 2)  # レベルアップしていることを確認
        self.assertEqual(user.target_achievement_count, 1)  # 1 件が残ることを確認

        remaining_targets = 5 - user.target_achievement_count
        self.assertEqual(remaining_targets, 4)  # 残り目標達成回数を確認
