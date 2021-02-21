#include <cstdio>
#include <algorithm>
#include <vector>
#include <utility>
#include <set>
using namespace std;


const int count_cups = 10000000; // количество чашек
const float mass_one_cup = 100; // в г размер одной кружки
const int mass_car = 3000000; // в г масса пустого грузовика

// Структура списка смежности
struct adjNode {
	int val, time;
	long int cost;
	adjNode* next;
};

// Структура дуг (это ребра, откуда -> куда, вес)
struct graphEdge {
	int start_ver, end_ver, time;
	long int weight;
};

class DiaGraph {
	private:
		// Число вершин
		int N;

		// Метод добавляющий новую вершину в граф
		adjNode* getAdjListNode(int value, int time, long int weight, adjNode* head) {
			adjNode* newNode = new adjNode;

			newNode->val = value;
			newNode->time = time;
			newNode->cost = weight;
			newNode->next = head;   // указать новый узел на текущую голову

			return newNode;
		}

	public:

		// Матрица смежности как массив указателей
		adjNode **head;            

		// Конструктор 
		DiaGraph(vector <graphEdge> edges, int n, int N);

		// Обход в ширину начиная с первой вершины
		bool Dijkstra(int N, int w);

		// Деструктор
		~DiaGraph() {
			for (int i = 0; i < N; i++)
				delete[] head[i];
				delete[] head;
		}
};

DiaGraph::DiaGraph(vector <graphEdge> edges, int n, int N) {

	head = new adjNode*[N]();
	this->N = N;

	// все вершины по умолчанию никуда не указывают, массив (количество вершин)
	for (int i = 0; i < N; ++i)
		head[i] = nullptr; // никуда указывающие вершины графа

	// строим ориентированный граф
	for (unsigned i = 0; i < n; i++) { 
		int start_ver = edges[i].start_ver;
		int end_ver = edges[i].end_ver;
		int time = edges[i].time;
		int weight = edges[i].weight;

		// формируем указатель предыдущей вершины в списке смежности на новую						
		adjNode* newNode = getAdjListNode(end_ver, time, weight, head[start_ver]); 

		// указатель head на новый узел
		head[start_ver] = newNode;
	}
}

// N - количество вершин
bool DiaGraph::Dijkstra(int N, int w)
{
	set<pair<int, int>> extract_set;

	vector<int> times(N, 1441); // кратчайшее время достижения вершин

	// инициализируем начальную вершину
	int num_start_vertex = 1;
	times[num_start_vertex] = 0;
	extract_set.insert(make_pair(0, 1)); // время до первой вершины == 0
	//


	adjNode* ptr;
	// сам цикл обхода
	while (!extract_set.empty())
	{
		// начало обхода, вытаскиваем вершину с мин. временем достижения
		pair<int, int> tmp = *(extract_set.begin());
		extract_set.erase(extract_set.begin());

		num_start_vertex = tmp.second; // получаем номер этой вершины
		ptr = head[num_start_vertex]; // начало обхода
		//
		
		while (ptr != nullptr)
		{
			if  ((times[ptr->val] > times[num_start_vertex] + ptr->time) && (ptr->cost >= w))
			{
				int num_visit_vertix = ptr->val;

				if (times[num_visit_vertix] != 1441) {
					extract_set.erase(extract_set.find(make_pair(times[num_visit_vertix], num_visit_vertix)));
				}

				// обновление значение времени достижения
				times[num_visit_vertix] = times[num_start_vertex] + ptr->time;
				extract_set.insert(make_pair(times[num_visit_vertix], num_visit_vertix));
			}
			ptr = ptr->next;
		}

	}

	if (times[N-1] < 1441) return true;
	else return false;

}

bool comp(graphEdge a, graphEdge b)
{
	return (a.weight < b.weight);
}

int main(void) {
	int N, M;

	long int right, left, mid; // для двоичного поиска по ответу
	int result_cups;
	scanf_s("%d%d", &N, &M);

	if (M == 0) // если нет дорог
	{
		if (N == 1) // если завод находится в месте проведения соревнования
		{
			printf("%d", count_cups);
		}
		else
		{
			printf("0");
		}
		
		return 0;
	}


	// получаем дуги
	vector <graphEdge> edges(M);
	for (int i = 0; i < M; i++)
	{
		scanf_s("%d%d%d%d", &edges[i].start_ver, &edges[i].end_ver, &edges[i].time, &edges[i].weight);
	}

	// строим граф 
	DiaGraph diagraph(edges, M, N + 1);

	auto minmax = minmax_element(edges.begin(), edges.end(), comp);
	right = (minmax.first)->weight;
	left = (minmax.second)->weight;

	// обрабатываем выход за границы
	if ( (left - mass_car)/ mass_one_cup > count_cups)
	{
		left = mass_car + mass_one_cup * count_cups;
	}
	
	int ans = diagraph.Dijkstra(N + 1, left);
	if (ans == true)
	{
		result_cups = (left - mass_car)/mass_one_cup;
		printf("%d", result_cups);
		return 0;
	}

	// по умолчанию пункт назначения не был достигнут
	ans = -1;

	while (right + 1 < left) // двоичный поиск по ответу
	{
		mid = (right + left) / 2;
		ans = diagraph.Dijkstra(N + 1, mid); //удалось ли попасть в пункт назначения с весом mid

		if (ans == false) left = mid;
		else right = mid;
	}
	if (ans == -1)  // если пункт назначения не достижим при любом весе
	{
		printf("0");
	}
	else 
	{
		result_cups = (right - mass_car) / mass_one_cup;
		printf("%d", result_cups);
	}


	return 0;
	
}